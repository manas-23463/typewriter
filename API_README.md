# Audio Typewriter API

A FastAPI server that accepts audio file uploads and returns generated typewriter videos with sentence-by-sentence effects.

## Features

- 🎵 **Audio Upload**: Accepts MP3, WAV, M4A, FLAC, OGG files
- 🎬 **Video Generation**: Creates MP4 videos with typewriter effects
- ⏱️ **Perfect Sync**: Text appears exactly when words are spoken
- 🔄 **Sentence Transitions**: Each sentence appears and disappears cleanly
- 📁 **File Download**: Returns the generated video as a downloadable file

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API server:**
   ```bash
   python3 api_server.py
   ```

   The server will start on `http://localhost:8000`

## API Endpoints

### GET `/`
- **Description**: API information and available endpoints
- **Response**: JSON with API details

### GET `/health`
- **Description**: Health check endpoint
- **Response**: `{"status": "healthy", "message": "API is running"}`

### POST `/create-video`
- **Description**: Upload audio file and get typewriter video
- **Input**: Audio file (multipart form data)
- **Output**: MP4 video file download
- **Supported formats**: MP3, WAV, M4A, FLAC, OGG

## Usage Examples

### 1. Using the Test Client

```bash
# Start the API server
python3 api_server.py

# In another terminal, test with an audio file
python3 test_api.py your_audio.mp3
```

### 2. Using cURL

```bash
# Upload audio file and download video
curl -X POST "http://localhost:8000/create-video" \
     -F "audio_file=@your_audio.mp3" \
     --output typewriter_video.mp4
```

### 3. Using Python Requests

```python
import requests

# Upload audio file
with open('your_audio.mp3', 'rb') as f:
    files = {'audio_file': ('audio.mp3', f, 'audio/mpeg')}
    response = requests.post('http://localhost:8000/create-video', files=files)

# Save the video
if response.status_code == 200:
    with open('output_video.mp4', 'wb') as f:
        f.write(response.content)
    print("Video created successfully!")
```

### 4. Using JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('audio_file', audioFile);

fetch('http://localhost:8000/create-video', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'typewriter_video.mp4';
    a.click();
});
```

## API Response

### Success Response
- **Status Code**: 200
- **Content-Type**: `video/mp4`
- **Body**: MP4 video file
- **Headers**: 
  - `Content-Disposition: attachment; filename=<unique_id>_typewriter.mp4`

### Error Responses

#### 400 Bad Request
```json
{
    "detail": "Unsupported file type. Allowed: .mp3, .wav, .m4a, .flac, .ogg"
}
```

#### 500 Internal Server Error
```json
{
    "detail": "Error processing audio: <error_message>"
}
```

## File Structure

```
typewriter/
├── api_server.py          # FastAPI server
├── test_api.py           # Test client
├── typewriter.py         # Standalone script
├── requirements.txt      # Dependencies
├── output_videos/        # Generated videos (created automatically)
└── API_README.md         # This file
```

## Configuration

You can modify the video settings in `api_server.py`:

```python
class AudioTypewriterVideo:
    def __init__(self, fps: int = 30):
        self.fps = fps
        self.width = 1280      # Video width
        self.height = 720      # Video height
        self.font_size = 80    # Font size
        self.margin = 100      # Text margin
```

## Performance Notes

- **Processing time**: Depends on audio length (typically 1-3x audio duration)
- **Memory usage**: Moderate (depends on video resolution and length)
- **Concurrent requests**: The server can handle multiple requests but processing is CPU-intensive
- **File cleanup**: Temporary files are automatically cleaned up after processing

## Troubleshooting

### Common Issues

1. **"Cannot connect to API"**
   - Make sure the server is running: `python3 api_server.py`
   - Check if port 8000 is available

2. **"Unsupported file type"**
   - Ensure your audio file is in a supported format
   - Check file extension is correct

3. **"Failed to transcribe audio"**
   - Audio file might be corrupted or too short
   - Try with a different audio file

4. **Slow processing**
   - Longer audio files take more time
   - Consider reducing video resolution for faster processing

### Server Logs

The API server provides detailed logs:
- Transcription progress
- Video rendering status
- Error messages
- Processing time

## Development

### Adding New Features

1. **New video effects**: Modify the `make_frame` function in `AudioTypewriterVideo`
2. **Additional endpoints**: Add new routes to the FastAPI app
3. **Custom configurations**: Add parameters to the API endpoints

### Testing

```bash
# Test API health
curl http://localhost:8000/health

# Test with sample audio
python3 test_api.py sample_audio.mp3
```

## License

This project is open source and available under the MIT License. 