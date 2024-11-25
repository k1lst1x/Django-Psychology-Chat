from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('chat', views.chatbot, name='chatbot'),
    path('video_callback', views.video_callback, name='video_callback'),
    path('rules', views.rules_page, name='rules')
    # path('', views.chatbot, name='chatbot'),
    # path('login', views.login, name='login'),
    # path('register', views.register, name='register'),
    # path('logout', views.logout, name='logout'),
]