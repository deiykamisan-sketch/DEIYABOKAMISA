"""OpenCV camera source used by the desktop air-writing mode."""
from __future__ import annotations
import cv2

class CameraSource:
    def __init__(self, source=0, width=1280, height=720):
        self.source, self.width, self.height = source, width, height
        self.capture = None

    def open(self):
        self.capture = cv2.VideoCapture(self.source)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if not self.capture.isOpened():
            raise RuntimeError(f'Cannot open camera source {self.source!r}')
        return self

    def read(self):
        if self.capture is None: self.open()
        ok, frame = self.capture.read()
        if not ok: raise RuntimeError('Camera stopped returning frames')
        return cv2.flip(frame, 1)

    def close(self):
        if self.capture is not None: self.capture.release()
        self.capture = None

    def __enter__(self): return self.open()
    def __exit__(self, *_): self.close()
