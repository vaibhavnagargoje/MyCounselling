# add pah and also give name for app 
from django.urls import path,include
from colleges import views

app_name = 'colleges'

urlpatterns = [
    # Define your URL patterns here
    path('', views.colleges, name='colleges'),
   ]