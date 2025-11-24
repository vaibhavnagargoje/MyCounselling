# add pah and also give name for app 
from django.urls import path,include
from collegepredictor import views

app_name = 'collegepredictor'

urlpatterns = [
    path('', views.college_predictor_home, name='college_predictor_home'),
]