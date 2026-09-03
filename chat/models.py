from django.conf import settings
from django.db import models
class StoredChatMessage(models.Model):
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='stored_chat_messages')
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text=models.CharField(max_length=500)
    is_question=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['created_at']
    def __str__(self): return f'{self.author}: {self.text[:40]}'
