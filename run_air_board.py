"""Desktop camera demo: ordinary green-tipped pen draws in the air. Press SPACE to lift, C to clear, Q to quit."""
import argparse
import cv2
from camera.camera import CameraSource
from camera.detector import ColorMarkerDetector
from pen_tracking.tracker import PenTracker
from whiteboard.drawing import DrawingLayer

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--camera',default='0');args=parser.parse_args()
    source=int(args.camera) if args.camera.isdigit() else args.camera
    detector=ColorMarkerDetector();tracker=PenTracker();drawing=None;drawing_enabled=True
    with CameraSource(source) as camera:
        while True:
            frame=camera.read()
            if drawing is None:drawing=DrawingLayer(frame.shape[1],frame.shape[0])
            detection,_=detector.detect(frame);point=tracker.update(detection) if drawing_enabled else None
            if point:drawing.draw(point);cv2.circle(frame,point,10,(0,255,0),2)
            else:drawing.lift()
            output=drawing.composite(frame);cv2.putText(output,'Q quit | C clear | SPACE pen up/down',(20,35),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2)
            cv2.imshow('AI Smart Lecture - Air Board',output);key=cv2.waitKey(1)&0xFF
            if key==ord('q'):break
            if key==ord('c'):drawing.clear()
            if key==32:drawing_enabled=not drawing_enabled;drawing.lift()
    cv2.destroyAllWindows()
if __name__=='__main__':main()
