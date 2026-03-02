import time

class TimerCore:
    def __init__(self, index):
        self.index = index
        self.running = False
        self.target_time = 0
        self.original_minutes = "00"
        self.original_seconds = "00"
        self.message = ""

    def start(self, minutes, seconds, message):
        if self.running:
            return False

        try:
            total_seconds = int(minutes) * 60 + int(seconds)
        except ValueError:
            total_seconds = 0
            
        if total_seconds <= 0:
             return False

        self.original_minutes = minutes
        self.original_seconds = seconds
        self.message = message
        self.target_time = time.time() + total_seconds
        self.running = True
        return True

    def stop(self):
        self.running = False

    def get_remaining_time(self):
        if not self.running:
            return 0
        return max(0, self.target_time - time.time())
        
    def get_remaining_time_formatted(self):
        remaining = self.get_remaining_time()
        mins, secs = divmod(int(remaining), 60)
        return f"{mins:02d}", f"{secs:02d}"

    def reset(self):
        self.running = False
