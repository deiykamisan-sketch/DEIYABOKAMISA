"""Optional MediaPipe fingertip tracker; the color-marker tracker works without it."""
class HandTrackingUnavailable(RuntimeError): pass

class FingertipTracker:
    def __init__(self):
        try:
            import mediapipe as mp
        except ImportError as exc:
            raise HandTrackingUnavailable('Install mediapipe to enable fingertip tracking') from exc
        self.cv=None; self.hands=mp.solutions.hands.Hands(max_num_hands=1,min_detection_confidence=.6,min_tracking_confidence=.6)

    def detect(self, frame):
        import cv2
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB); result=self.hands.process(rgb)
        if not result.multi_hand_landmarks: return None
        tip=result.multi_hand_landmarks[0].landmark[8]; h,w=frame.shape[:2]
        return int(tip.x*w),int(tip.y*h)
