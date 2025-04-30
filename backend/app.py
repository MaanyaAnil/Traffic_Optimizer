from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse # Import FileResponse
from fastapi import FastAPI, HTTPException
import os
import shutil
import subprocess
import json
from typing import List, Literal, Tuple, Dict, Any
import time  # For simulating real-time delay
import asyncio  # Import asyncio for running subprocess asynchronously
from detector import process_video_with_yolov8  # Import the function, not the whole module
from emergency import EmergencyManager
from optimizer import dynamic_signal_timing
import logging

# Initialize logging
logging.basicConfig(level=logging.ERROR)  # Set level as needed
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the upload folder if it doesn't exist (optional, but good for robustness)
UPLOAD_FOLDER = "upload"
PROCESSED_UPLOAD_FOLDER = "processed_upload"

if not os.path.exists(PROCESSED_UPLOAD_FOLDER):
    os.makedirs(PROCESSED_UPLOAD_FOLDER)
if not os.path.exists(UPLOAD_FOLDER): #create upload folder
    os.makedirs(UPLOAD_FOLDER)

# Initialize emergency manager
emergency_manager = EmergencyManager()


# Route: Health Check
@app.get("/")
def read_root():
    return {"message": "AI Traffic Flow Optimizer API is running"}


# Route: Upload Traffic Videos
@app.post("/upload")
async def upload_videos(videos: List[UploadFile] = File(...)):
    if len(videos) != 4:
        return JSONResponse(content={"error": "Exactly 4 videos required (North, South, East, West)"}, status_code=400)

    vehicle_counts = []
    processed_video_filenames = []
    for video in videos:
        uploaded_path = os.path.join(UPLOAD_FOLDER, video.filename)
        try:
            with open(uploaded_path, "wb") as buffer:
                content = await video.read()
                buffer.write(content)  # Write the video content to the file

            logger.debug(f"Uploaded video to: {uploaded_path}")  # Debug log

            processed_path, count = process_video_with_yolov8(uploaded_path, PROCESSED_UPLOAD_FOLDER)  # Pass the folder

            if processed_path:
                processed_video_filenames.append(os.path.basename(processed_path))
                vehicle_counts.append(count)
                logger.debug(f"Processed video: {processed_path}, Count: {count}")  # Debug log
            else:
                logger.warning(f"Failed to process {video.filename}")
                vehicle_counts.append(0)  # Use 0 count if processing failed
                processed_video_filenames.append(None)  # Indicate processing failure

            os.remove(uploaded_path)  # Clean up uploaded file

        except Exception as e:
            logger.error(f"Error saving/processing video {video.filename}: {e}", exc_info=True)
            return JSONResponse(
                content={"error": f"Error saving video {video.filename}: {e}"}, status_code=500
            )

    emergency_direction = emergency_manager.get_emergency_direction()
    optimized_timings = dynamic_signal_timing(vehicle_counts, emergency_direction)

    print(f"Backend Response - processed_videos: {processed_video_filenames}")
    return {
        "optimized_timings": optimized_timings,
        "processed_videos": processed_video_filenames,
    }


# Route: Trigger Emergency Mode
@app.post("/emergency")
def trigger_emergency(direction: str):
    if direction.lower() not in ['north', 'south', 'east', 'west']:
        return JSONResponse(content={"error": "Invalid direction"}, status_code=400)
    
    emergency_manager.trigger_emergency(direction.lower())
    return {"message": f"Emergency triggered for {direction}"}

# Route: Clear Emergency Mode
@app.post("/emergency/clear")
def clear_emergency():
    emergency_manager.clear_emergency()
    return {"message": "Emergency cleared"}

# Route: Get Current Status
@app.get("/status")
def get_status():
    return {
        "emergency_mode": emergency_manager.is_emergency_active(),
        "emergency_direction": emergency_manager.get_emergency_direction()
    }


@app.get("/processed_video/{filename}")
async def get_processed_video(filename: str):
    video_path = os.path.join(PROCESSED_UPLOAD_FOLDER, filename)
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    else:
        raise HTTPException(status_code=404, detail="Processed video not found")

