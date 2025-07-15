from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'chatting'
urlpatterns = [
    path('', views.chatting, name='chatting'),
    path("test/",views.test,name="test"),
    path("start_chat/",views.start_chat,name="start_chat"),
    # path("room/<str:room_name>/",views.room,name="room"),
    path('fetch-messages/<int:room_id>/', views.fetch_messages, name='fetch_messages'),
    path("cancel_chat/<int:room_id>/",views.cancel_chat,name="cancel_chat"),
    path("block_user/<str:target_id>/",views.block_user,name="block_user"),
    path("change_poststate/<str:target_id>/",views.change_poststate,name="change_poststate"),
]
