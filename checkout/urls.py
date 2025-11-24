from django.urls import path,include
from . import views

app_name = 'checkout'

urlpatterns = [
    path("", views.checkout, name="checkout_page"),

   
]
	