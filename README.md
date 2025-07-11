# Audio Typewriter Video Creator

A Python script that transcribes audio files using OpenAI Whisper and creates videos with typewriter effects synced to the actual audio timing.

## Features

- 🎵 Transcribes audio files (.mp3, .wav, .m4a, .flac, .ogg) with precise timestamps
- 🎬 Creates MP4 videos with typewriter effects synced to audio timing
- ⏱️ Two sync modes: segment-based and character-by-character
- 🖥️ Full HD video output (1920x1080) with clean typography
- 📁 Automatically saves videos in the same folder as the audio file
- 🎯 Perfect synchronization - text appears exactly when words are spoken

## Requirements

- Python 3.7 or higher
- macOS, Windows, or Linux
- FFmpeg (for video processing)

## Installation

1. **Clone or download this repository**

2. **Install FFmpeg** (required for video processing):
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install openai-whisper moviepy numpy pillow
   ```

## Usage

### Method 1: Interactive Selection
Run the script to see available audio files and select one:
```bash
python3 typewriter.py
```

### Method 2: Command Line
Provide the audio file path directly:
```bash
python3 typewriter.py path/to/your/audio.mp3
```

## Video Types

The script offers two synchronization modes:

### 1. Segment-Synced (Recommended)
- Text appears segment by segment as spoken
- More natural reading experience
- Faster rendering
- Output: `filename_typewriter.mp4`

### 2. Character-Synced (Advanced)
- Each character appears individually synced to audio
- More precise timing but slower rendering
- Output: `filename_typewriter_synced.mp4`

## How it Works

1. **Audio Analysis**: Uses Whisper with word-level timestamps to extract precise timing
2. **Video Creation**: Generates a white background with black text
3. **Synchronization**: Text appears exactly when words are spoken in the audio
4. **Output**: Creates an MP4 file with the original audio and synced text

## Output Files

- **Segment-synced**: `your_audio_typewriter.mp4`
- **Character-synced**: `your_audio_typewriter_synced.mp4`
- Files are saved in the same directory as the input audio

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)

## Customization

You can modify these parameters in the `AudioTypewriterVideo` class:

- **Video resolution**: Change `self.width = 1920` and `self.height = 1080`
- **Font size**: Adjust `self.font_size = 48`
- **Margins**: Modify `self.margin = 100`
- **Frame rate**: Change `fps = 30` in the constructor

## Performance Tips

- **Short audio files** (1-5 minutes) render quickly
- **Long audio files** (10+ minutes) may take 10-30 minutes to render
- **Character-synced mode** is slower but more precise
- **Segment-synced mode** is faster and usually sufficient

## Troubleshooting

### Common Issues

1. **"No module named 'moviepy'"**
   - Install dependencies: `pip install -r requirements.txt`

2. **FFmpeg not found**
   - Install FFmpeg: `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Linux)

3. **Slow rendering**
   - Use segment-synced mode for faster results
   - Reduce video resolution in the code
   - Use shorter audio files

4. **Audio file not supported**
   - Convert to MP3 or WAV format
   - Ensure the file is not corrupted

5. **Out of memory errors**
   - Use shorter audio files
   - Reduce video resolution
   - Close other applications

### Performance Optimization

- **RAM**: 4GB+ recommended for longer videos
- **Storage**: Ensure 2-3x audio file size for output video
- **CPU**: Multi-core processors will render faster

## Example Output

For a 2-minute audio file:
- **Input**: `speech.mp3` (2:30 duration)
- **Output**: `speech_typewriter.mp4` (2:30 duration)
- **Sync**: Text appears exactly when words are spoken
- **Quality**: Full HD with clear, readable typography

## License

This project is open source and available under the MIT License. 