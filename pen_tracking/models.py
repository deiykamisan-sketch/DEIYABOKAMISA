from django.conf import settings
from django.db import models
class PenCalibration(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='pen_calibrations')
    camera=models.ForeignKey('camera.CameraDevice',on_delete=models.CASCADE,related_name='calibrations')
    matrix=models.JSONField(default=dict)
    color_lower=models.JSONField(default=list)
    color_upper=models.JSONField(default=list)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Calibration · {self.user}'
