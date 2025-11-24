from django.urls import path
from . import views
from django.contrib import admin

app_name = 'products'  # ADD THIS for best practice
urlpatterns = [
    path("", views.products_plans, name="products"),
    path("<str:type>/<slug:slug>/", views.product_detail, name="product_detail"),
]