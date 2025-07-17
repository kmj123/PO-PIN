from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('chgReview/main/', views.chgReviewmain, name='chgReviewmain'),
    path('chgReview/view/<int:pk>/', views.chgReviewview, name='chgReviewview'),
   
    path('recent/', views.recent, name='recent'),
    path('write/companion/', views.write_companion, name='write_companion'),
    path('write/proxy/', views.write_proxy, name='write_proxy'),
    path('write/review/', views.write_review, name='write_review'),
    path('write/sharing/', views.write_sharing, name='write_sharing'),
    path('write/status/', views.write_status, name='write_status'),


    path('', views.main, name='main'),

    path('companion/', views.companion, name='companion'),
    path('proxy/', views.proxy, name='proxy'),
    path('sharing/', views.sharing, name='sharing'),
    path('status/', views.status, name='status'),

    path('report_post/<str:post_type>/<int:post_id>/', views.report_post, name='report_post'),
    # 수정
    path('updateCo/<int:pk>/', views.updateCo, name='updateCo'),
    path('updateP/<int:pk>/', views.updateP, name='updateP'),
    path('updateSh/<int:pk>/', views.updateSh, name='updateSh'),
    path('updateS/<int:pk>/', views.updateS, name='updateS'),
    # 상세페이지 
    path('companion/<int:pk>/', views.companionview, name='companionview'),
    path('proxy/<int:pk>/', views.proxyview, name='proxyview'),
    path('sharing/<int:pk>/', views.sharingview, name='sharingview'),
    path('status/<int:pk>/', views.statusview, name='statusview'),
    
    path('mypage_community_list/', views.mypage_community_list, name='mypage_community_list'),
]