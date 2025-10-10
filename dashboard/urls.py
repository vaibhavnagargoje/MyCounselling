from django.urls import path,include
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('home/', include(('home.urls', 'home'), namespace='home')),
    path('colleges/', include(('colleges.urls', 'colleges'), namespace='colleges')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    # path('doubts/', include(('doubts.urls', 'doubts'), namespace='doubts')),
    # path('store/', include(('store.urls', 'store'), namespace='store')),
    # path('library/', include(('library.urls', 'library'), namespace='library')),
    # path('support/', include(('support.urls', 'support'), namespace='support')),
    # path('performance/', include(('performance.urls', 'performance'), namespace='performance')),
]
	