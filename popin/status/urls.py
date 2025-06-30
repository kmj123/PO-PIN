from django.urls import path, include
from.import views

app_name = 'status'
urlpatterns = [
    path('',views.main,name='main'),
]
