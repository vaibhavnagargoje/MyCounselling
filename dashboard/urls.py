from django.urls import path,include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    # path('colleges/', include(('colleges.urls', 'colleges'), namespace='colleges')),
    # path('doubts/', include(('doubts.urls', 'doubts'), namespace='doubts')),
    # path('store/', include(('store.urls', 'store'), namespace='store')),
    # path('library/', include(('library.urls', 'library'), namespace='library')),
    # path('support/', include(('support.urls', 'support'), namespace='support')),
    # path('performance/', include(('performance.urls', 'performance'), namespace='performance')),
]
	