# add pah and also give name for app 
from django.urls import path, include
from . import views

app_name = 'colleges'

urlpatterns = [
    # Define your URL patterns here
    path('', views.colleges_list, name='colleges_list'),
    path('<int:college_id>/', views.college_detail, name='college_detail'),
   ]