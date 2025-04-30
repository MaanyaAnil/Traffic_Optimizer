# tests/test_performance.py
from optimizer import dynamic_signal_timing  # Import the dynamic_signal_timing function

def test_performance(benchmark):
    """
    Performance test: Measure the performance of the signal timing calculation.
    """
    vehicle_counts = [10000, 10000, 10000, 10000]
    result = benchmark(dynamic_signal_timing, vehicle_counts)
    assert result['north'] > 0  # Ensure result is returned

