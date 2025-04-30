def dynamic_signal_timing(vehicle_counts, emergency_direction=None):
    """
    Calculate green signal timings dynamically based on vehicle counts.
    If emergency mode is active, override to give 60s green for that direction.
    
    Parameters:
    - vehicle_counts: List[int] -> Number of vehicles [North, South, East, West]
    - emergency_direction: str or None -> Direction where ambulance is detected
    
    Returns:
    - dict: {'north': seconds, 'south': seconds, 'east': seconds, 'west': seconds}
    """
    
    # Handle emergency override first
    if emergency_direction:
        return {
            'north': 60 if emergency_direction == 'north' else 0,
            'south': 60 if emergency_direction == 'south' else 0,
            'east': 60 if emergency_direction == 'east' else 0,
            'west': 60 if emergency_direction == 'west' else 0
        }

    # Normal traffic optimization
    total_vehicles = sum(vehicle_counts)
    
    # Avoid division by zero
    if total_vehicles == 0:
        return {'north': 10, 'south': 10, 'east': 10, 'west': 10}
    
    timings = {}
    directions = ['north', 'south', 'east', 'west']
    
    for idx, direction in enumerate(directions):
        proportion = vehicle_counts[idx] / total_vehicles
        seconds = int(proportion * 120)  # Full cycle 120 seconds
        seconds = max(10, min(seconds, 60))  # Clamp between 10s and 60s
        timings[direction] = seconds
    
    return timings
