from django.urls import path, include
from.import views

app_name = 'sharing'
urlpatterns = [
    path('',views.main,name='main'),
]
