from django.urls import path, include
from . import views

app_name = 'photocard'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('view/<int:pno>/', views.view, name='view'),
    path('write/', views.write, name='write'),
    path('update/<int:pno>/', views.update, name='update'),
    path('delete/<int:pno>/', views.delete, name='delete'),
]
