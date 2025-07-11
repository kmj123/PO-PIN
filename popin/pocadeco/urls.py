
from django.urls import path
from . import views

app_name = 'pocadeco'

urlpatterns = [
    path('main/', views.main, name='main'), # 포꾸하는곳 (메인)
    path('decolist/', views.decolist, name='decolist'), #포꾸리스트
    path('view/<int:id>/', views.view, name='view'), #포꾸 상세보기

    # path('mydecolist/', views.mydecolist, name='mydecolist'), 

]