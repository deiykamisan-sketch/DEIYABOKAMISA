from django.contrib import admin
from .models import ChatMessage, Lecture, LiveParticipant, LiveSession, Question, WhiteboardSnapshot

admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(WhiteboardSnapshot)
admin.site.register(LiveSession)
admin.site.register(LiveParticipant)
admin.site.register(ChatMessage)
# Register your models here.
