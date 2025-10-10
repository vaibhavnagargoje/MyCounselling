from django.urls import path
from . import views
from django.contrib import admin

app_name = 'products'  # ADD THIS for best practice
urlpatterns = [
    path("", views.all_products, name="products"),
]