from django.db import models
class LectureRecording(models.Model):
    STATES=[('recording','Recording'),('processing','Processing'),('ready','Ready'),('failed','Failed')]
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='recordings')
    state=models.CharField(max_length=12,choices=STATES,default='recording')
    video_file=models.FileField(upload_to='recordings/video/',blank=True)
    duration_seconds=models.PositiveIntegerField(default=0)
    started_at=models.DateTimeField(auto_now_add=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    def __str__(self): return f'{self.lecture} · {self.state}'
