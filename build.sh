#!/bin/bash

# Update package list and install system dependencies
apt-get update
apt-get install -y ffmpeg fonts-liberation fonts-dejavu gcc g++

# Upgrade pip and install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create output directory
mkdir -p output_videos

echo "Build completed successfully!" 