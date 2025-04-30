import time

class EmergencyManager:
    def __init__(self):
        self.active = False
        self.direction = None
        self.trigger_time = None

    def trigger_emergency(self, direction):
        self.active = True
        self.direction = direction
        self.trigger_time = time.time()  # Record when it started

    def clear_emergency(self):
        self.active = False
        self.direction = None
        self.trigger_time = None

    def get_emergency_direction(self):
        if self.active:
            # Automatically clear after 60 seconds
            if time.time() - self.trigger_time > 60:
                self.clear_emergency()
                return None
            return self.direction
        return None

    def is_emergency_active(self):
        # Similar logic to check if active and auto-clear
        if self.active and (time.time() - self.trigger_time > 60):
            self.clear_emergency()
        return self.active
