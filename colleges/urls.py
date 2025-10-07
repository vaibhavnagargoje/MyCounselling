# add pah and also give name for app 
from django.urls import path,include
from colleges import views

app_name = 'colleges'

urlpatterns = [
    # Define your URL patterns here
    path('', views.colleges, name='colleges'),
    path('<int:college_id>/', views.college_detail, name='college_detail'),
   ]