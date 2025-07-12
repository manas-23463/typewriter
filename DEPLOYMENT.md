# Deploying Audio Typewriter API on Render

This guide will help you deploy the Audio Typewriter API on Render as a web service.

## Prerequisites

- A Render account (free tier available)
- Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Options

### Option 1: Using render.yaml (Recommended)

1. **Push your code to GitHub** with the `render.yaml` file
2. **Connect your repository to Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration

### Option 2: Manual Deployment

1. **Create a new Web Service:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure the service:**
   - **Name:** `audio-typewriter-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api_server:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables:**
   - `PYTHON_VERSION`: `3.9.16`

4. **Add Disk (Optional):**
   - **Name:** `video-storage`
   - **Mount Path:** `/opt/render/project/src/output_videos`
   - **Size:** `10 GB`

## Important Considerations

### ⚠️ **Free Tier Limitations**

- **Build time:** 15 minutes max
- **Request timeout:** 30 seconds
- **Sleep after inactivity:** 15 minutes
- **No persistent disk storage** (videos will be lost)

### 💡 **Production Recommendations**

1. **Upgrade to paid plan** for:
   - Persistent disk storage
   - Longer build times
   - No sleep mode
   - Better performance

2. **Use external storage** (AWS S3, Google Cloud Storage) for video files

3. **Add rate limiting** to prevent abuse

4. **Configure CORS** properly for your domain

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `OUTPUT_DIR` | Video output directory | `output_videos` |

## API Endpoints

Once deployed, your API will be available at:
`https://your-app-name.onrender.com`

### Health Check
```
GET https://your-app-name.onrender.com/health
```

### Create Video
```
POST https://your-app-name.onrender.com/create-video
```

## Testing the Deployment

### Using cURL
```bash
# Health check
curl https://your-app-name.onrender.com/health

# Upload audio file
curl -X POST "https://your-app-name.onrender.com/create-video" \
     -F "audio_file=@your_audio.mp3" \
     --output typewriter_video.mp4
```

### Using Postman
1. **Health Check:**
   - Method: `GET`
   - URL: `https://your-app-name.onrender.com/health`

2. **Create Video:**
   - Method: `POST`
   - URL: `https://your-app-name.onrender.com/create-video`
   - Body: `form-data`
   - Key: `audio_file` (Type: File)

## Troubleshooting

### Common Issues

1. **Build fails:**
   - Check if all dependencies are in `requirements.txt`
   - Ensure FFmpeg is properly installed (handled by Dockerfile)

2. **Service times out:**
   - Audio files are too large
   - Processing takes too long
   - Upgrade to paid plan for longer timeouts

3. **Videos not persisting:**
   - Free tier doesn't have persistent storage
   - Use external storage or upgrade plan

4. **Font issues:**
   - Dockerfile includes common fonts
   - Check font paths in the code

### Logs

Check Render dashboard for:
- Build logs
- Runtime logs
- Error messages

## Performance Optimization

1. **Reduce video quality** for faster processing
2. **Limit file size** (add validation)
3. **Use async processing** for long videos
4. **Implement caching** for repeated requests

## Security Considerations

1. **File size limits** (add validation)
2. **File type validation** (already implemented)
3. **Rate limiting** (recommended)
4. **CORS configuration** (configure for your domain)

## Cost Estimation

### Free Tier
- $0/month
- Limited features
- Good for testing

### Paid Plans
- **Starter:** $7/month
- **Standard:** $25/month
- **Pro:** $85/month

Choose based on your expected usage and requirements. 