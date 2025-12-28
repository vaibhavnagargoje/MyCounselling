from django.urls import path, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('courses/', include(('course_delivery.urls', 'course_delivery'), namespace='course_delivery')),
]

	