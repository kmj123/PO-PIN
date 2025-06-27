from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'admin'
urlpatterns = [
    path('', views.main, name='main'),
    path('user/', views.user, name='user'),
    path('post/', views.post, name='post'),
    path('postV/', views.postV, name='postV'),
    path('notice/', views.notice, name='notice'),
    path('noticeV/', views.noticeV, name='noticeV'),
    path('noticeW/', views.noticeW, name='noticeW'),
]
