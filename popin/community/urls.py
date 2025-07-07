from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.main, name='main'),
    path('write/review/', views.write_review, name='write_review'),
    path('write/companion/', views.write_companion, name='write_companion'),
    path('write/proxy/', views.write_proxy, name='write_proxy'),
    path('write/status/', views.status, name='status'),
    
    path('recent/', views.recent, name='recent'),
    #
    path('chgReview/', views.chgReview, name='chgReview'),
    path('chgReview/main/', views.chgReviewmain, name='chgReviewmain'),
    path('chgReview/view/', views.chgReviewview, name='chgReviewview'),
    
    path('companion/', views.companion, name='companion'),
    path('proxy/', views.proxy, name='proxy'),
    path('status/', views.status, name='status'),
    
    
    path('sharing/', views.sharing, name='sharing'),
    path('write/sharing/', views.write_sharing, name='write_sharing'),
   
]