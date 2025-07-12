#!/usr/bin/env python3
"""
Audio Typewriter API Server

FastAPI server that accepts audio file uploads and returns generated typewriter videos.

Requirements:
- fastapi
- uvicorn
- python-multipart
- whisper
- moviepy
- numpy
- pillow

Install dependencies:
pip install fastapi uvicorn python-multipart openai-whisper moviepy numpy pillow
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import os
import tempfile
import uuid
from typing import List
from moviepy.editor import AudioFileClip, VideoClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import shutil


class AudioTypewriterVideo:
    def __init__(self, fps: int = 30):
        self.fps = fps
        self.width = 1280
        self.height = 720
        self.font_size = 80
        self.margin = 100
        self.font_path = self._find_font()

    def _find_font(self):
        # Try to find a bold sans-serif font
        for font in [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS system font
            "/System/Library/Fonts/Arial.ttf",      # macOS Arial
            "/Library/Fonts/Arial Bold.ttf",        # Bold Arial
            "/Library/Fonts/Helvetica.ttc",         # Helvetica
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",  # Linux
            "Arial.ttf", 
            "arial.ttf", 
            "/Library/Fonts/Arial.ttf"
        ]:
            if os.path.exists(font):
                return font
        # Fallback to default PIL font
        return None

    def transcribe_with_segments(self, audio_path: str) -> List[dict]:
        """
        Transcribe audio file using Whisper with segment timing
        """
        try:
            print(f"Loading Whisper model...")
            model = whisper.load_model("base")
            
            print(f"Transcribing audio file: {audio_path}")
            result = model.transcribe(audio_path, word_timestamps=True)
            
            return result["segments"]
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return []

    def create_sentence_typewriter_video(self, audio_path: str, segments: List[dict], output_path: str) -> str:
        """
        Create a video with sentence-by-sentence typewriter effect
        """
        print("Creating sentence-by-sentence typewriter video...")
        
        # Load audio to get duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # Prepare font
        if self.font_path:
            font = ImageFont.truetype(self.font_path, self.font_size)
        else:
            font = ImageFont.load_default()

        def make_frame(t):
            # Find which segment should be displayed at time t
            current_segment = None
            for segment in segments:
                if segment['start'] <= t <= segment['end']:
                    current_segment = segment
                    break
            
            # Create white background
            img = Image.new("RGB", (self.width, self.height), color="white")
            draw = ImageDraw.Draw(img)
            
            if current_segment:
                segment_text = current_segment['text'].strip()
                segment_start = current_segment['start']
                segment_end = current_segment['end']
                
                # Calculate how much of the sentence should be shown
                segment_duration = segment_end - segment_start
                elapsed_in_segment = t - segment_start
                
                # Calculate how many characters to show based on time
                total_chars = len(segment_text)
                if segment_duration > 0:
                    chars_to_show = int((elapsed_in_segment / segment_duration) * total_chars)
                else:
                    chars_to_show = total_chars
                
                chars_to_show = min(chars_to_show, total_chars)
                current_text = segment_text[:chars_to_show]
                
                # Word wrap the current text
                lines = []
                words = current_text.split(' ')
                line = ''
                
                for word in words:
                    test_line = line + (' ' if line else '') + word
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    w = bbox[2] - bbox[0]
                    
                    if w < self.width - 2 * self.margin:
                        line = test_line
                    else:
                        if line:  # Only add non-empty lines
                            lines.append(line)
                        line = word
                
                if line:  # Add the last line
                    lines.append(line)
                
                # Draw text centered
                y = self.margin
                for l in lines:
                    bbox = draw.textbbox((0, 0), l, font=font)
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                    x = (self.width - w) // 2
                    draw.text((x, y), l, font=font, fill="black")
                    y += h + 15
                
                # Blinking cursor at the end
                if int(t * 2) % 2 == 0 and chars_to_show < total_chars:
                    if lines:
                        last_line = lines[-1]
                        bbox = draw.textbbox((0, 0), last_line, font=font)
                        w = bbox[2] - bbox[0]
                        h = bbox[3] - bbox[1]
                        x = (self.width - w) // 2 + w
                        y_cursor = self.margin + (len(lines) - 1) * (h + 15)
                    else:
                        x = self.margin
                        y_cursor = self.margin
                    draw.text((x, y_cursor), "|", font=font, fill="black")

            return np.array(img)

        video = VideoClip(make_frame, duration=duration)
        video = video.set_audio(audio_clip)
        
        print(f"Rendering video to: {output_path}")
        
        video.write_videofile(
            output_path,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        audio_clip.close()
        video.close()
        return output_path


# Create FastAPI app
app = FastAPI(
    title="Audio Typewriter API",
    description="API for creating typewriter videos from audio files",
    version="1.0.0"
)

# Add CORS middleware for web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create output directory
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output_videos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global video creator instance
video_creator = AudioTypewriterVideo()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Audio Typewriter API",
        "version": "1.0.0",
        "endpoints": {
            "/create-video": "POST - Upload audio file and get typewriter video",
            "/health": "GET - Check API health"
        },
        "deployment": "Render"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


@app.post("/create-video")
async def create_typewriter_video(audio_file: UploadFile = File(...)):
    """
    Create a typewriter video from uploaded audio file
    
    Args:
        audio_file: Audio file (MP3, WAV, M4A, FLAC, OGG)
    
    Returns:
        Video file with typewriter effect
    """
    # Validate file type
    allowed_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
    file_extension = os.path.splitext(audio_file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Create unique filename
    unique_id = str(uuid.uuid4())
    temp_audio_path = f"/tmp/{unique_id}_audio{file_extension}"
    output_filename = f"{unique_id}_typewriter.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    try:
        # Save uploaded file
        with open(temp_audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        # Transcribe audio
        print(f"Processing audio file: {audio_file.filename}")
        segments = video_creator.transcribe_with_segments(temp_audio_path)
        
        if not segments:
            raise HTTPException(status_code=500, detail="Failed to transcribe audio")
        
        print(f"Transcription completed! Found {len(segments)} segments.")
        
        # Create video
        video_creator.create_sentence_typewriter_video(temp_audio_path, segments, output_path)
        
        # Return video file
        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="video/mp4",
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )
        
    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")
        
    finally:
        # Clean up temporary files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 