from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login, name='login'),
    path('id/', views.id, name='id'),
    path('pw/', views.pw, name='pw'),
    path('chgpw/', views.chgpw, name='chgpw'),
]
