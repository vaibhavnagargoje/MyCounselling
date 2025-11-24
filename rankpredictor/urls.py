# add pah and also give name for app 
from django.urls import path,include
from rankpredictor import views

app_name = 'rank_predictor'

urlpatterns = [
    path('', views.rank_predictor_home, name='rank_predictor_home'),
]