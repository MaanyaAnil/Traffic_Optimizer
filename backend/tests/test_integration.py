import os
from detector import detect_vehicles
from optimizer import dynamic_signal_timing  # ✅ Make sure this import is included

def test_end_to_end_flow():
    """
    End-to-end test: From vehicle detection to traffic signal timing.
    """
    # Build the full path to the test video
    video_path = os.path.join(os.path.dirname(__file__), "test_video.mp4")
    
    # Step 1: Run vehicle detection
    vehicle_count = detect_vehicles(video_path)
    assert vehicle_count > 0  # Ensure vehicles are detected

    # Step 2: Use the detected vehicle count in signal timing logic
    vehicle_counts = [vehicle_count, 10, 5, 15]  # Simulated input
    timings = dynamic_signal_timing(vehicle_counts)

    # Step 3: Verify the optimized timings
    assert timings['north'] > 0
    assert timings['south'] > 0
    assert timings['east'] > 0
    assert timings['west'] > 0
