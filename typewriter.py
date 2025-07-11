#!/usr/bin/env python3
"""
Audio Typewriter - Creates video with sentence-by-sentence typewriter effect

This script takes an audio file, transcribes it using OpenAI Whisper with segments,
and creates a video showing each sentence appearing with typewriter effect as it's spoken.

Requirements:
- whisper
- moviepy
- numpy
- pillow

Install dependencies:
pip install openai-whisper moviepy numpy pillow
"""

import whisper
import os
import sys
from typing import List, Optional
from moviepy.editor import AudioFileClip, VideoClip
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class AudioTypewriterVideo:
    def __init__(self, fps: int = 30):
        self.fps = fps
        self.width = 1280
        self.height = 720
        self.font_size = 80  # Adjusted for sentence display
        self.margin = 100
        self.font_path = self._find_font()

    def _find_font(self):
        # Try to find a bold sans-serif font
        for font in [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS system font
            "/System/Library/Fonts/Arial.ttf",      # macOS Arial
            "/Library/Fonts/Arial Bold.ttf",        # Bold Arial
            "/Library/Fonts/Helvetica.ttc",         # Helvetica
            "Arial.ttf", 
            "arial.ttf", 
            "/Library/Fonts/Arial.ttf", 
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ]:
            if os.path.exists(font):
                return font
        # Fallback to default PIL font
        return None

    def transcribe_with_segments(self, audio_path: str) -> List[dict]:
        """
        Transcribe audio file using Whisper with segment timing
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            List of segments with timing information
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

    def create_sentence_typewriter_video(self, audio_path: str, segments: List[dict]) -> str:
        """
        Create a video with sentence-by-sentence typewriter effect
        
        Args:
            audio_path: Path to the audio file
            segments: List of transcription segments with timing
            
        Returns:
            Path to the created video file
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

        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = f"{base_name}_sentence_typewriter.mp4"
        
        print(f"Rendering video to: {output_path}")
        print("This may take a few minutes...")
        
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


def select_audio_file() -> Optional[str]:
    print("\nAvailable audio files in current directory:")
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
    audio_files = [f for f in os.listdir('.') if any(f.lower().endswith(ext) for ext in audio_extensions)]
    
    if not audio_files:
        print("No audio files found in current directory.")
        return None
    
    for i, file in enumerate(audio_files, 1):
        print(f"{i}. {file}")
    
    try:
        choice = input(f"\nSelect audio file (1-{len(audio_files)}) or enter path: ").strip()
        
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(audio_files):
                return audio_files[index]
        elif os.path.exists(choice):
            return choice
        
        print("Invalid selection.")
        return None
        
    except KeyboardInterrupt:
        print("\nCancelled.")
        return None


def main():
    print("Audio Typewriter Video Creator (Sentence-by-sentence)")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        if not os.path.exists(audio_path):
            print(f"Error: File '{audio_path}' not found.")
            return
    else:
        audio_path = select_audio_file()
        if not audio_path:
            print("No file selected. Exiting.")
            return
    
    creator = AudioTypewriterVideo()
    
    print("Starting transcription with segments...")
    segments = creator.transcribe_with_segments(audio_path)
    
    if not segments:
        print("Failed to transcribe audio. Exiting.")
        return
    
    print(f"Transcription completed! Found {len(segments)} segments.")
    
    # Show segments info
    for i, segment in enumerate(segments, 1):
        print(f"Segment {i}: {segment['start']:.1f}s - {segment['end']:.1f}s")
        print(f"  Text: {segment['text'].strip()}")
    
    output_path = creator.create_sentence_typewriter_video(audio_path, segments)
    
    print(f"\n✅ Video created successfully!")
    print(f"📁 Output file: {output_path}")
    print(f"📊 File size: {os.path.getsize(output_path) / (1024*1024):.1f} MB")


if __name__ == "__main__":
    main() 