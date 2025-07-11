#!/usr/bin/env python3
"""
Test client for Audio Typewriter API

This script demonstrates how to use the API to create typewriter videos.
"""

import requests
import os
import sys


def test_api_health():
    """Test the API health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API is healthy!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on localhost:8000")
        return False


def upload_audio_file(audio_file_path):
    """Upload an audio file and get the typewriter video"""
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
        return None
    
    try:
        print(f"📤 Uploading audio file: {audio_file_path}")
        
        with open(audio_file_path, 'rb') as f:
            files = {'audio_file': (os.path.basename(audio_file_path), f, 'audio/mpeg')}
            response = requests.post("http://localhost:8000/create-video", files=files)
        
        if response.status_code == 200:
            # Save the video file
            output_filename = f"api_output_{os.path.splitext(os.path.basename(audio_file_path))[0]}.mp4"
            
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Video created successfully!")
            print(f"📁 Output file: {output_filename}")
            print(f"📊 File size: {len(response.content) / (1024*1024):.1f} MB")
            
            return output_filename
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return None


def main():
    print("Audio Typewriter API Test Client")
    print("=" * 40)
    
    # Test API health
    if not test_api_health():
        print("\nPlease start the API server first:")
        print("python3 api_server.py")
        return
    
    # Get audio file path
    if len(sys.argv) > 1:
        audio_file_path = sys.argv[1]
    else:
        # Look for audio files in current directory
        audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
        audio_files = [f for f in os.listdir('.') if any(f.lower().endswith(ext) for ext in audio_extensions)]
        
        if not audio_files:
            print("❌ No audio files found in current directory.")
            print("Usage: python3 test_api.py <audio_file_path>")
            return
        
        print("\nAvailable audio files:")
        for i, file in enumerate(audio_files, 1):
            print(f"{i}. {file}")
        
        try:
            choice = input(f"\nSelect audio file (1-{len(audio_files)}) or enter path: ").strip()
            
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(audio_files):
                    audio_file_path = audio_files[index]
                else:
                    print("Invalid selection.")
                    return
            else:
                audio_file_path = choice
                
        except KeyboardInterrupt:
            print("\nCancelled.")
            return
    
    # Upload and process
    print(f"\n🚀 Processing audio file: {audio_file_path}")
    result = upload_audio_file(audio_file_path)
    
    if result:
        print(f"\n🎉 Success! Your typewriter video is ready: {result}")


if __name__ == "__main__":
    main() 