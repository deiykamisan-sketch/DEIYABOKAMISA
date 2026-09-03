from django.db import models
class TranscriptSegment(models.Model):
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='transcript_segments')
    speaker=models.CharField(max_length=120,blank=True)
    text=models.TextField()
    start_ms=models.PositiveBigIntegerField(default=0)
    end_ms=models.PositiveBigIntegerField(default=0)
    confidence=models.FloatField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['start_ms']
    def __str__(self): return f'{self.speaker}: {self.text[:40]}'
