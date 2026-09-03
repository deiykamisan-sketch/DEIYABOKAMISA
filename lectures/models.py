import secrets
import string
from django.conf import settings
from django.db import models
from django.urls import reverse


def share_code():
    return secrets.token_urlsafe(12)


class Lecture(models.Model):
    PRIVACY = [('private', 'Private'), ('shared', 'Shared')]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=180)
    subject = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY, default='private')
    share_token = models.CharField(max_length=32, unique=True, default=share_code, editable=False)
    video = models.FileField(upload_to='lectures/video/', blank=True)
    audio = models.FileField(upload_to='lectures/audio/', blank=True)
    attachment = models.FileField(upload_to='lectures/files/', blank=True)
    transcript = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lecture_detail', args=[self.pk])


class WhiteboardSnapshot(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='snapshots')
    original_drawing = models.TextField(help_text='Canvas image as a data URL')
    recognized_text = models.TextField(blank=True)
    drawing_type = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='questions')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


def lecture_code():
    alphabet = string.ascii_uppercase + string.digits
    return '-'.join(''.join(secrets.choice(alphabet) for _ in range(n)) for n in (3, 4))


class LiveSession(models.Model):
    lecture = models.OneToOneField(Lecture, on_delete=models.CASCADE, related_name='live_session')
    code = models.CharField(max_length=8, unique=True, default=lecture_code, editable=False)
    is_live = models.BooleanField(default=True)
    whiteboard_state = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)


class LiveParticipant(models.Model):
    session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    raised_hand = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['session', 'user'], name='one_live_participant')]


class ChatMessage(models.Model):
    session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
