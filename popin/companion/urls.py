from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'companion'
urlpatterns = [
    path('', views.main, name='main'),
]
