from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'admin'
urlpatterns = [
    path('user/', views.user, name='user'),
    # path('id/', views.id, name='id'),
    # path('pw/', views.pw, name='pw'),
    # path('chgpw/', views.chgpw, name='chgpw'),
]
