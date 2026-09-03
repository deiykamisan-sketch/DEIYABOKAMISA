"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('lectures.urls')),
    path('modules/accounts/', include('accounts.urls')),
    path('modules/users/', include('users.urls')),
    path('modules/live/', include('live_sessions.urls')),
    path('modules/whiteboard/', include('whiteboard.urls')),
    path('modules/camera/', include('camera.urls')),
    path('modules/pen/', include('pen_tracking.urls')),
    path('modules/recording/', include('recording.urls')),
    path('modules/speech/', include('speech.urls')),
    path('modules/ai/', include('ai.urls')),
    path('modules/questions/', include('questions.urls')),
    path('modules/realtime/', include('realtime.urls')),
    path('modules/chat/', include('chat.urls')),
    path('modules/notifications/', include('notifications.urls')),
    path('modules/sharing/', include('sharing.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
