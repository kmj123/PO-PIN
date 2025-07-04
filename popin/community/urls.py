from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('write_review/', views.write_review, name='write_review'),
    path('write_sharing/', views.write_sharing, name='write_sharing'),
]