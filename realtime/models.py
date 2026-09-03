from django.conf import settings
from django.db import models
class SignalingMessage(models.Model):
    session=models.ForeignKey('lectures.LiveSession',on_delete=models.CASCADE,related_name='signals')
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    target_user_id=models.PositiveBigIntegerField(null=True,blank=True)
    signal_type=models.CharField(max_length=20)
    payload=models.JSONField(default=dict)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.signal_type} from {self.sender}'
