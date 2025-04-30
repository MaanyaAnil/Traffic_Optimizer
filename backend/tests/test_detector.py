import os
import cv2
import numpy as np
from detector import process_video_with_yolov8
from detector import detect_vehicles

def test_vehicle_detection_valid_video():
    video_path = "test_video.mp4"
    vehicle_count = detect_vehicles(video_path)
    assert vehicle_count > 0  # Expecting some vehicles detected

def test_vehicle_detection_empty_video():
    video_path = "empty_video.mp4"
    vehicle_count = detect_vehicles(video_path)
    assert vehicle_count == 0  # No vehicles detected in empty video

# Utility: Create a fake video for testing
def create_dummy_video(path, num_frames=10, width=640, height=480):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, 10, (width, height))
    for _ in range(num_frames):
        frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        out.write(frame)
    out.release()

def test_process_video_with_dummy():
    input_path = "tests/test_input.mp4"
    output_dir = "tests/processed"

    os.makedirs(output_dir, exist_ok=True)
    create_dummy_video(input_path)

    processed_path, count = process_video_with_yolov8(input_path, output_dir)

    assert processed_path is not None
    assert os.path.exists(processed_path)
    assert isinstance(count, int)

    # Clean up
    os.remove(input_path)
    os.remove(processed_path)
