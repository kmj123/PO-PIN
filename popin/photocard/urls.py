from django.urls import path, include
from . import views

app_name = 'photocard'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('view/<int:pno>/', views.view, name='view'),
]
