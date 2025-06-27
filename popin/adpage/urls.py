from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'admin'
urlpatterns = [
    path('', views.main, name='main'),                      # 관리자 대시보드
    path('user/', views.user, name='user'),                 # 사용자관리
    path('post/', views.post, name='post'),                 # 게시글관리
    path('postV/', views.postV, name='postV'),              # 게시글상세보기
    path('notice/', views.notice, name='notice'),           # 공지사항
    path('noticeV/', views.noticeV, name='noticeV'),        # 공지사항 상세보기
    path('noticeW/', views.noticeW, name='noticeW'),        # 공지사항 작성
]
