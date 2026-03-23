import time

class TimerCore:
    def __init__(self, index):
        self.index = index
        self.running = False
        self.target_time = 0
        self.original_hours = "00"
        self.original_minutes = "00"
        self.original_seconds = "00"
        self.message = ""

    def start(self, hours, minutes, seconds, message):
        if self.running:
            return False

        try:
            total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        except ValueError:
            total_seconds = 0
            
        if total_seconds <= 0:
             return False

        self.original_hours = hours
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
        total_secs = int(remaining)
        hours, remainder = divmod(total_secs, 3600)
        mins, secs = divmod(remainder, 60)
        return f"{hours:02d}", f"{mins:02d}", f"{secs:02d}"

    def restart(self):
        """將計時器重置回原始設定時間，從現在重新倒數。"""
        if not self.running:
            return False
        try:
            total_seconds = (int(self.original_hours) * 3600
                             + int(self.original_minutes) * 60
                             + int(self.original_seconds))
        except ValueError:
            return False
        if total_seconds <= 0:
            return False
        self.target_time = time.time() + total_seconds
        return True

    def reset(self):
        self.running = False
