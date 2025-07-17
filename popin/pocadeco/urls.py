
from django.urls import path
from . import views

app_name = 'pocadeco'

urlpatterns = [
    path('main/', views.main, name='main'), # 포꾸하는곳 (메인)
    path('decolist/', views.decolist, name='decolist'), #포꾸리스트
    path('view/<int:id>/', views.view, name='view'), #포꾸 상세보기
    path('save_decopoca/', views.save_decopoca, name='save_decopoca'), #포꾸 서버에 저장
    path('delete_decopoca/', views.delete_decopoca, name='delete_decopoca'), #포꾸 서버에 저장
    path('decoview/<int:id>/', views.decoview, name='decoview'),
    path('toggle_wish/<int:id>/', views.toggle_wish, name='toggle_wish'),
    path('get_idol_data/', views.get_idol_data, name='get_idol_data'), #아이돌 데이터 가져오기
    # path('mydecolist/', views.mydecolist, name='mydecolist'), 

]