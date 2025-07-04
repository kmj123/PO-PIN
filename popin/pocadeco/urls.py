from django.urls import path, include
from . import views

app_name = 'pocadeco'
urlpatterns = [
    path('decoMain/', views.decoMain, name='decoMain'),
]
