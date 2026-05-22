class TimerEngine:
    def __init__(self, duration_minutes=25):
        self.duration = duration_minutes * 60
        self.remaining = self.duration
        self.running = False

    def reset(self):
        self.remaining = self.duration
        self.running = False

    def toggle(self):
        self.running = not self.running
        return self.running

    def tick(self):
        if self.running and self.remaining > 0:
            self.remaining -= 1
            return True
        return False