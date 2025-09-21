# add pah and also give name for app 
from django.urls import path,include
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
]