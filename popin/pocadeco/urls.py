
from django.urls import path
from . import views

app_name = 'pocadeco'

urlpatterns = [
    path('main/', views.main, name='main'), 
    # path('mydecolist/', views.mydecolist, name='mydecolist'), 
    path('decoMain/', views.decoMain, name='decoMain'), 
    path('view/<int:id>/', views.view, name='view'), 
]