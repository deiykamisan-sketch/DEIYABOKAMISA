from django.conf import settings
from django.db import models
class CameraDevice(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='camera_devices')
    label=models.CharField(max_length=120)
    device_key=models.CharField(max_length=255)
    is_phone=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    def __str__(self): return self.label
