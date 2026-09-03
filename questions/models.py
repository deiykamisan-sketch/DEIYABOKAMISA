from django.conf import settings
from django.db import models
class LiveQuestion(models.Model):
    STATES=[('new','New'),('viewed','Viewed'),('important','Important'),('answered','Answered'),('deferred','Deferred')]
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='live_questions')
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text=models.TextField()
    source=models.CharField(max_length=10,choices=[('chat','Chat'),('voice','Voice')],default='chat')
    state=models.CharField(max_length=12,choices=STATES,default='new')
    answer=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.text[:60]
