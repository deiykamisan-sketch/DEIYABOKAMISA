from django.db import models
class AIArtifact(models.Model):
    KINDS=[('ocr','OCR'),('summary','Summary'),('diagram','Diagram'),('answer','Answer suggestion')]
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='ai_artifacts')
    kind=models.CharField(max_length=12,choices=KINDS)
    input_reference=models.CharField(max_length=255,blank=True)
    output_text=models.TextField()
    approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.kind} · {self.lecture}'
