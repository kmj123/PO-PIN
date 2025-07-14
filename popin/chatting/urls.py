from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'chatting'
urlpatterns = [
    path('', views.chatting, name='chatting'),
    path("test/",views.test,name="test"),
    path("start_chat/",views.start_chat,name="start_chat"),
    # path("room/<str:room_name>/",views.room,name="room"),
]
