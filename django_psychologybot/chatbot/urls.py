from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('chat', views.chatbot, name='chatbot'),
    path('upload_video', views.upload_video, name='upload_video')
    # path('', views.chatbot, name='chatbot'),
    # path('login', views.login, name='login'),
    # path('register', views.register, name='register'),
    # path('logout', views.logout, name='logout'),
]