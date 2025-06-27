from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'login'
urlpatterns = [
    path('loginp/', views.loginp, name='loginp'), #로그인 
    path('loginID/', views.loginID, name='loginID'), # 아이디 찾기 
    path('loginPW/', views.loginPW, name='loginPW'), # 비번 찾기 
    path('loginCPW/', views.loginCPW, name='loginCPW'),# 비밀번호 재설정
    path('send_code/', views.send_verification_code, name='send_code'),
]
