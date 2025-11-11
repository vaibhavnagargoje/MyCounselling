# add pah and also give name for app 
from django.urls import path,include
from landing_page import views

app_name = 'landing_page'

urlpatterns = [
    # Define your URL patterns here
    path('', views.index, name='index'),
    path('colleges/', views.colleges, name='colleges'),
    path('college-details/<int:college_id>/', views.college_details, name='college_details'),
    path('college-predictor/',views.college_predictor, name='college_predictor'),
    path('rank-predictor/',views.rank_predictor, name='rank_predictor'),
    path('about-us/',views.about_us, name='about_us'),
    path('careers/',views.careers, name='careers'),

]