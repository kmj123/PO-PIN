from django.urls import path, include
from.import views

app_name = 'proxy'
urlpatterns = [
    path('',views.main,name='main'),
]
