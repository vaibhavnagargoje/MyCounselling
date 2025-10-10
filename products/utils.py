"""
User Subscription Management Utilities
Helper functions to check user access, manage subscriptions, etc.
"""

from django.utils import timezone
from django.db.models import Q
from .models import UserSubscription, Service, Plan


class SubscriptionManager:
    """Manager class for handling user subscriptions"""
    
    def __init__(self, user):
        self.user = user
    
    def has_active_subscription(self, service_slug=None, service_type=None):
        """
        Check if user has active subscription for a service or service type
        """
        query = Q(
            user=self.user,
            status='active',
            is_active=True,
            expiry_date__gt=timezone.now()
        )
        
        if service_slug:
            query &= Q(service__slug=service_slug)
        
        if service_type:
            query &= Q(service__service_type=service_type)
        
        return UserSubscription.objects.filter(query).exists()
    
    def get_active_subscriptions(self):
        """Get all active subscriptions for user"""
        return UserSubscription.objects.filter(
            user=self.user,
            status='active',
            is_active=True,
            expiry_date__gt=timezone.now()
        ).select_related('service', 'plan', 'order')
    
    def get_subscription_for_service(self, service_slug):
        """Get active subscription for specific service"""
        return UserSubscription.objects.filter(
            user=self.user,
            service__slug=service_slug,
            status='active',
            is_active=True,
            expiry_date__gt=timezone.now()
        ).select_related('service', 'plan', 'order').first()
    
    def get_expired_subscriptions(self):
        """Get all expired subscriptions for user"""
        return UserSubscription.objects.filter(
            user=self.user,
            expiry_date__lte=timezone.now()
        ).select_related('service', 'plan', 'order')
    
    def get_expiring_soon(self, days=7):
        """Get subscriptions expiring within specified days"""
        expiry_threshold = timezone.now() + timezone.timedelta(days=days)
        return UserSubscription.objects.filter(
            user=self.user,
            status='active',
            is_active=True,
            expiry_date__lte=expiry_threshold,
            expiry_date__gt=timezone.now()
        ).select_related('service', 'plan', 'order')
    
    def access_service(self, service_slug):
        """
        Record service access and return subscription info
        Returns: (has_access, subscription, message)
        """
        subscription = self.get_subscription_for_service(service_slug)
        
        if not subscription:
            return False, None, "You don't have an active subscription for this service."
        
        # Check if expired
        if not subscription.is_valid():
            subscription.check_and_update_status()
            return False, subscription, "Your subscription has expired."
        
        # Record access
        subscription.record_access()
        
        return True, subscription, "Access granted."
    
    def get_subscription_summary(self):
        """Get summary of user's subscriptions"""
        active = self.get_active_subscriptions()
        expiring_soon = self.get_expiring_soon()
        expired = self.get_expired_subscriptions()
        
        return {
            'active_count': active.count(),
            'active_subscriptions': active,
            'expiring_soon_count': expiring_soon.count(),
            'expiring_soon': expiring_soon,
            'expired_count': expired.count(),
            'total_subscriptions': active.count() + expired.count()
        }
    
    def can_purchase_plan(self, plan):
        """
        Check if user can purchase a plan
        Returns: (can_purchase, message)
        """
        if not plan.is_active:
            return False, "This plan is not available."
        
        # Check max purchases limit
        if plan.max_purchases_per_user > 0:
            user_purchases = UserSubscription.objects.filter(
                user=self.user,
                plan=plan
            ).count()
            
            if user_purchases >= plan.max_purchases_per_user:
                return False, f"You have reached the maximum purchase limit for this plan."
        
        return True, "You can purchase this plan."
    
    def get_services_with_access(self):
        """Get list of service slugs user has access to"""
        active_subscriptions = self.get_active_subscriptions()
        return [sub.service.slug for sub in active_subscriptions]
    
    def has_purchased_service(self, service_slug):
        """Check if user has ever purchased a service (active or expired)"""
        return UserSubscription.objects.filter(
            user=self.user,
            service__slug=service_slug
        ).exists()


def check_service_access(user, service_slug):
    """
    Decorator helper to check if user has access to a service
    Usage: has_access, subscription, message = check_service_access(request.user, 'jee-counselling')
    """
    manager = SubscriptionManager(user)
    return manager.access_service(service_slug)


def get_user_active_services(user):
    """Get list of all services user has active access to"""
    manager = SubscriptionManager(user)
    return manager.get_services_with_access()


def update_expired_subscriptions():
    """
    Utility function to update status of expired subscriptions
    Can be run as a cron job or celery task
    """
    expired_subscriptions = UserSubscription.objects.filter(
        status='active',
        is_active=True,
        expiry_date__lte=timezone.now()
    )
    
    count = 0
    for subscription in expired_subscriptions:
        subscription.status = 'expired'
        subscription.is_active = False
        subscription.save()
        count += 1
    
    return count


def send_expiry_notifications():
    """
    Send notifications to users whose subscriptions are expiring soon
    Can be run as a cron job or celery task
    """
    # Get subscriptions expiring in 7 days
    expiry_threshold = timezone.now() + timezone.timedelta(days=7)
    expiring_subscriptions = UserSubscription.objects.filter(
        status='active',
        is_active=True,
        expiry_date__lte=expiry_threshold,
        expiry_date__gt=timezone.now()
    ).select_related('user', 'service')
    
    notifications_sent = 0
    for subscription in expiring_subscriptions:
        # Send email notification
        # send_email_notification(subscription.user, subscription)
        notifications_sent += 1
    
    return notifications_sent


def get_popular_plans(limit=3):
    """Get popular plans"""
    return Plan.objects.filter(
        is_active=True,
        is_popular=True
    ).order_by('display_order')[:limit]


def get_featured_plans(limit=6):
    """Get featured plans"""
    return Plan.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('display_order')[:limit]


def get_all_active_plans():
    """Get all active plans"""
    return Plan.objects.filter(
        is_active=True
    ).prefetch_related('services').order_by('display_order', 'name')


def get_services_by_category(category_slug=None):
    """Get services optionally filtered by category"""
    queryset = Service.objects.filter(is_active=True)
    
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    
    return queryset.order_by('display_order', 'name')


def get_services_by_type(service_type):
    """Get services by type (counselling, predictor, etc.)"""
    return Service.objects.filter(
        is_active=True,
        service_type=service_type
    ).order_by('display_order', 'name')


def get_services_by_exam(exam_type):
    """Get services by exam type"""
    return Service.objects.filter(
        is_active=True,
        exam_type=exam_type
    ).order_by('display_order', 'name')
