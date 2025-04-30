# tests/test_optimizer.py
from optimizer import dynamic_signal_timing

def test_dynamic_signal_timing_normal():
    """
    Test for dynamic signal timing with normal traffic counts.
    """
    vehicle_counts = [10, 20, 30, 40]
    result = dynamic_signal_timing(vehicle_counts)
    assert result['north'] > 0
    assert result['south'] > 0
    assert result['east'] > 0
    assert result['west'] > 0

def test_dynamic_signal_timing_emergency():
    """
    Test for dynamic signal timing with emergency override.
    """
    vehicle_counts = [10, 10, 10, 10]
    result = dynamic_signal_timing(vehicle_counts, emergency_direction="north")
    assert result['north'] == 60
    assert result['south'] == 0
    assert result['east'] == 0
    assert result['west'] == 0
