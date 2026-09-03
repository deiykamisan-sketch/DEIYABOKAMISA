"""Computer-vision pen-tracking adapter boundary."""

class PenPoint:
    def __init__(self, x, y, detected=True):
        self.x, self.y, self.detected = x, y, detected
