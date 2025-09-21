# add pah and also give name for app 
from django.urls import path,include
from landing_page import views

app_name = 'landing_page'

urlpatterns = [
    # Define your URL patterns here
    path('', views.index, name='index'),
]