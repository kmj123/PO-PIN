from django.urls import path, include
from.import views

app_name = 'chgReview'
urlpatterns = [
    path('',views.main,name='main'),
]
