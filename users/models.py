from django.conf import settings
from django.db import models
class UserPreference(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='lecture_preferences')
    language=models.CharField(max_length=10,default='en')
    email_notifications=models.BooleanField(default=True)
    high_contrast=models.BooleanField(default=False)
    def __str__(self): return f'Preferences: {self.user}'
