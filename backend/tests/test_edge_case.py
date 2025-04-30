# tests/test_edge_cases.py
from optimizer import dynamic_signal_timing

def test_dynamic_signal_timing_zero_vehicles():
    """
    Test for zero vehicle counts (empty traffic scenario).
    """
    vehicle_counts = [0, 0, 0, 0]
    result = dynamic_signal_timing(vehicle_counts)
    assert result['north'] == 10
    assert result['south'] == 10
    assert result['east'] == 10
    assert result['west'] == 10

def test_dynamic_signal_timing_high_vehicle_counts():
    """
    Test for a very high number of vehicles (stress test).
    """
    vehicle_counts = [100000, 100000, 100000, 100000]
    result = dynamic_signal_timing(vehicle_counts)
    assert result['north'] > 0
    assert result['south'] > 0
    assert result['east'] > 0
    assert result['west'] > 0
