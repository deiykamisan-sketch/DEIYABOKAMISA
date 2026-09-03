from django.conf import settings
from django.db import models
class AttendanceRecord(models.Model):
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='attendance_records')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    joined_at=models.DateTimeField(auto_now_add=True)
    left_at=models.DateTimeField(null=True,blank=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['lecture','user'],name='unique_lecture_attendee')]
    def __str__(self): return f'{self.user} · {self.lecture}'
