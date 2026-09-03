"""Transparent OpenCV drawing layer used by desktop air writing."""
import cv2
import numpy as np

class DrawingLayer:
    def __init__(self,width,height,color=(30,30,240),thickness=5):
        self.canvas=np.zeros((height,width,4),dtype=np.uint8); self.color=color; self.thickness=thickness; self.previous=None
    def draw(self,point):
        if point and self.previous: cv2.line(self.canvas,self.previous,point,(*self.color,255),self.thickness,cv2.LINE_AA)
        self.previous=point
    def lift(self): self.previous=None
    def clear(self): self.canvas[:]=0; self.previous=None
    def undo_snapshot(self): return self.canvas.copy()
    def restore(self,snapshot): self.canvas=snapshot.copy(); self.previous=None
    def composite(self,frame,opacity=.9):
        alpha=(self.canvas[:,:,3:4].astype(np.float32)/255)*opacity
        rgb=self.canvas[:,:,:3].astype(np.float32)
        return (frame.astype(np.float32)*(1-alpha)+rgb*alpha).astype(np.uint8)
