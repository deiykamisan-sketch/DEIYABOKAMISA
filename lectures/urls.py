from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lectures/new/', views.lecture_create, name='lecture_create'),
    path('lectures/<int:pk>/', views.lecture_detail, name='lecture_detail'),
    path('lectures/<int:pk>/snapshot/', views.save_snapshot, name='save_snapshot'),
    path('lectures/<int:pk>/questions/', views.add_question, name='add_question'),
    path('lectures/<int:pk>/live/start/', views.start_live, name='start_live'),
    path('join/', views.join_live, name='join_live'),
    path('live/<str:code>/', views.live_room, name='live_room'),
    path('live/<str:code>/api/', views.live_api, name='live_api'),
    path('live/<str:code>/signals/', views.signal_api, name='signal_api'),
    path('live/<str:code>/recording/', views.upload_recording, name='upload_recording'),
    path('share/<str:token>/', views.shared_lecture, name='shared_lecture'),
]
