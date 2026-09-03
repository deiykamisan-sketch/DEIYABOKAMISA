from django.conf import settings
from django.db import models
class UserRole(models.Model):
    ROLE_CHOICES=[('lecturer','Lecturer'),('student','Student'),('admin','Administrator')]
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='role_profile')
    role=models.CharField(max_length=12,choices=ROLE_CHOICES,default='student')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.user} · {self.role}'
