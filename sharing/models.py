import secrets
from django.db import models
def share_token(): return secrets.token_urlsafe(24)
class ShareLink(models.Model):
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='share_links')
    token=models.CharField(max_length=64,unique=True,default=share_token,editable=False)
    allow_download=models.BooleanField(default=False)
    expires_at=models.DateTimeField(null=True,blank=True)
    revoked=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Share · {self.lecture}'
