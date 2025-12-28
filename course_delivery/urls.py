from django.urls import path
from . import views

app_name = 'course_delivery'

urlpatterns = [
    # API endpoint for fetching course content
    path('api/content/', views.get_course_content_api, name='get_course_content'),
    path('api/content/<int:product_id>/', views.get_course_content_api, name='get_course_content_by_product'),
    
    # Detail pages
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('resource/<int:resource_id>/', views.resource_detail, name='resource_detail'),
]
