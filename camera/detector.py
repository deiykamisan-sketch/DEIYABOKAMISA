"""Color-marker detector for an ordinary ink pen."""
from dataclasses import dataclass
import cv2
import numpy as np

@dataclass(frozen=True)
class Detection:
    x: int
    y: int
    area: float

class ColorMarkerDetector:
    def __init__(self, lower=(35, 70, 70), upper=(90, 255, 255), min_area=80):
        self.lower=np.array(lower,dtype=np.uint8); self.upper=np.array(upper,dtype=np.uint8); self.min_area=min_area

    def detect(self, frame):
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,self.lower,self.upper)
        mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
        contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if not contours: return None,mask
        contour=max(contours,key=cv2.contourArea); area=cv2.contourArea(contour)
        if area<self.min_area: return None,mask
        moments=cv2.moments(contour)
        if not moments['m00']: return None,mask
        return Detection(int(moments['m10']/moments['m00']),int(moments['m01']/moments['m00']),area),mask
