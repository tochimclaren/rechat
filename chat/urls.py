from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_home, name='chat_home'),
    path('save/', views.save_chat, name='save_chat')
]