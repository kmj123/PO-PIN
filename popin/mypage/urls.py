from django.urls import path, include
from.import views

app_name = 'mypage'
urlpatterns = [
    path('profile/',views.profile,name='profile'),
    path('pchange/',views.pchange,name='pchange'),
    path('keyword/', views.keyword, name='keyword'),
    path('test/', views.test, name='test'),
    path('mypoca/', views.my_poca, name='my_poca'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('trade/', views.trade, name='trade'),
]
