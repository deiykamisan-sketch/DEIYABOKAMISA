"""Smooth pen coordinates and decide when a stroke is continuous."""
from collections import deque

class PenTracker:
    def __init__(self, smoothing=5, max_jump=140):
        self.points=deque(maxlen=smoothing); self.max_jump=max_jump; self.previous=None
    def update(self, detection):
        if detection is None: self.points.clear(); self.previous=None; return None
        point=(detection.x,detection.y)
        if self.previous and ((point[0]-self.previous[0])**2+(point[1]-self.previous[1])**2)**.5>self.max_jump:
            self.points.clear()
        self.points.append(point); self.previous=point
        return (round(sum(p[0] for p in self.points)/len(self.points)),round(sum(p[1] for p in self.points)/len(self.points)))
