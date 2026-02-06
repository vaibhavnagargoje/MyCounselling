"""
Dynamic Sitemaps for E-Counselling
Auto-generates sitemap.xml with all pages including 2500+ college detail pages.
This replaces the static sitemap.xml for SEO - Google will auto-discover all college URLs.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from colleges.models import EngineeringCollege


class StaticViewSitemap(Sitemap):
    """Sitemap for all static/landing pages"""
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'landing_page:index',
            'landing_page:about_us',
            'landing_page:tools_and_services',
            'landing_page:contact',
            'landing_page:careers',
            'landing_page:privacy_policy',
            'landing_page:terms_of_service',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'landing_page:index': 1.0,
            'landing_page:tools_and_services': 0.9,
            'landing_page:about_us': 0.8,
            'landing_page:contact': 0.7,
            'landing_page:careers': 0.7,
            'landing_page:privacy_policy': 0.3,
            'landing_page:terms_of_service': 0.3,
        }
        return priorities.get(item, 0.5)

    def changefreq(self, item):
        if item == 'landing_page:index':
            return 'daily'
        elif item in ['landing_page:privacy_policy', 'landing_page:terms_of_service']:
            return 'yearly'
        return 'weekly'


class ToolsSitemap(Sitemap):
    """Sitemap for free tools pages - HIGH priority for tool-related searches"""
    priority = 0.9
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'rank_predictor:rank_predictor_home',
            'college_predictor:college_predictor_home',
            'colleges:colleges_list',
        ]

    def location(self, item):
        return reverse(item)


class CollegeDetailSitemap(Sitemap):
    """
    Dynamic sitemap for individual college pages.
    This is the KEY for ranking on "XYZ college placement record" searches.
    Google will discover and index every single college page.
    """
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return EngineeringCollege.objects.filter(is_active=True).order_by('id')

    def location(self, obj):
        return reverse('colleges:college_detail', args=[obj.id])

    def lastmod(self, obj):
        return obj.updated_at


class UserPagesSitemap(Sitemap):
    """Sitemap for user auth pages"""
    priority = 0.5
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return [
            'user:login',
            'user:register',
        ]

    def location(self, item):
        return reverse(item)


# Combined sitemaps dict for urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'tools': ToolsSitemap,
    'colleges': CollegeDetailSitemap,
    'user': UserPagesSitemap,
}
