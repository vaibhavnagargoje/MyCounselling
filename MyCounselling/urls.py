"""
URL configuration for MyCounselling project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import FileResponse, HttpResponse
from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps
import os

# View functions for SEO files
def serve_robots(request):
    file_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'robots.txt')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    # Fallback inline robots.txt
    content = """User-agent: *
Allow: /
Sitemap: https://ecounselling.live/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')

def serve_sitemap(request):
    """Fallback - dynamic sitemap is at /sitemap.xml via Django sitemaps framework"""
    file_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'sitemap.xml')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/xml')
    return HttpResponse('<urlset></urlset>', content_type='application/xml')

def serve_llms(request):
    file_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'llms.txt')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    return HttpResponse('E-Counselling - NEET, JEE, MHT-CET Counselling Platform', content_type='text/plain')

def serve_ai_manifest(request):
    file_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'ai-manifest.json')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/json')
    return HttpResponse('{}', content_type='application/json')

def serve_security_txt(request):
    """Serve security.txt file as per RFC 9116"""
    file_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', '.well-known', 'security.txt')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    return HttpResponse('Contact: support@ecounselling.in', content_type='text/plain')

def serve_humans_txt(request):
    """Serve humans.txt file - credits for the team"""
    file_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR / 'static', 'humans.txt')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    return HttpResponse('/* TEAM */ E-Counselling', content_type='text/plain')

urlpatterns = [
    # SEO & AI Discovery Files (must be at root level)
    path('robots.txt', serve_robots, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('llms.txt', serve_llms, name='llms'),
    path('humans.txt', serve_humans_txt, name='humans'),  # Team credits
    path('ai-manifest.json', serve_ai_manifest, name='ai_manifest'),
    path('.well-known/ai-manifest.json', serve_ai_manifest, name='ai_manifest_well_known'),
    path('.well-known/security.txt', serve_security_txt, name='security_txt'),  # RFC 9116
    
    path('my-secure-admin-panel/', admin.site.urls),
    # add path and namespace also
    path('',include('landing_page.urls',namespace='landing_page')),
    path('rankpredictor/',include('rankpredictor.urls', namespace='rank_predictor')),
    path('collegepredictor/',include('collegepredictor.urls', namespace='college_predictor')),
    path('colleges/', include(('colleges.urls', 'colleges'), namespace='colleges')),
    path('checkout/', include(('checkout.urls', 'checkout'), namespace='checkout')),

    path('user/',include('user.urls', namespace='user')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # In development static is auto-served when DEBUG=True; MEDIA needs explicit
if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
