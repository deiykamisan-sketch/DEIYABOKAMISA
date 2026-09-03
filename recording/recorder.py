"""Record composite OpenCV frames with the platform video encoder."""
import cv2
class VideoRecorder:
    def __init__(self,path,fps,size):
        self.path=path; self.writer=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*'mp4v'),fps,size)
        if not self.writer.isOpened(): raise RuntimeError('Cannot create video recording')
    def write(self,frame): self.writer.write(frame)
    def close(self): self.writer.release()
    def __enter__(self): return self
    def __exit__(self,*_): self.close()
