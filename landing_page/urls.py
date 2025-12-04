# add pah and also give name for app 
from django.urls import path,include
from landing_page import views

app_name = 'landing_page'

urlpatterns = [
    # Define your URL patterns here
    path('', views.index, name='index'),
    path('about-us/',views.about_us, name='about_us'),
    path('careers/',views.careers, name='careers'),
    path('tools-and-services/',views.tools_and_services, name='tools_and_services'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]