# Assuming your tests are in the backend/tests directory
from unittest.mock import patch
from detector import detect_vehicles  # Ensure you're importing the correct function

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_detector_with_mock(mock_detect_vehicles):
    """
    Test vehicle detection with mocked function.
    """
    mock_detect_vehicles.return_value = 5  # Mocking the vehicle count

    # Don't need the video file because we're mocking the function
    video_path = "test_video.mp4"  # Just a placeholder

    # Call the function, which should return the mocked value
    vehicle_count = detect_vehicles(video_path)

    # Ensure the mocked count is returned
    assert vehicle_count == 5

