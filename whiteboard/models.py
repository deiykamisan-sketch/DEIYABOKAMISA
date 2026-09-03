from django.db import models
class BoardPage(models.Model):
    lecture=models.ForeignKey('lectures.Lecture',on_delete=models.CASCADE,related_name='board_pages')
    page_number=models.PositiveIntegerField(default=1)
    canvas_data=models.TextField(blank=True)
    recognized_text=models.TextField(blank=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['lecture','page_number'],name='unique_board_page')]
    def __str__(self): return f'{self.lecture} · page {self.page_number}'
