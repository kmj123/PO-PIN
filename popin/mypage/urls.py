from django.urls import path, include
from.import views

app_name = 'mypage'
urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('pchange/',views.pchange,name='pchange'),
]
