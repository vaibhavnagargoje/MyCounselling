"""
User Subscription Management Utilities
Helper functions to check user access, manage subscriptions, etc.
"""

from django.utils import timezone
from django.db.models import Q
from .models import UserSubscription, MyProducts, BundledPlan


class SubscriptionManager:
    """Manager class for handling user subscriptions"""
    
    def __init__(self, user):
        self.user = user
    
    def has_active_subscription(self, product_slug=None, service_type=None):
        """
        Check if user has active subscription for a product or service type
        """
        query = Q(
            user=self.user,
            status='active',
            is_active=True,
            expiry_date__gt=timezone.now()
        )
        
        if product_slug:
            query &= Q(product__slug=product_slug)
        
        if service_type:
            query &= Q(product__service_type=service_type)
        
        return UserSubscription.objects.filter(query).exists()
    
    def get_active_subscriptions(self):
        """Get all active subscriptions for user"""
        return UserSubscription.objects.filter(
            user=self.user,
            status='active',
            is_active=True,
            expiry_date__gt=timezone.now()
        ).select_related('product', 'bundled_plan', 'order')
    
    def get_subscription_for_product(self, product_slug):
        """Get active subscription for specific product"""
        return UserSubscription.objects.filter(
            user=self.user,
            product__slug=product_slug,
            status='active',
            is_active=True,
            expiry_date__gt=timezone.now()
        ).select_related('product', 'bundled_plan', 'order').first()
    
    def get_expired_subscriptions(self):
        """Get all expired subscriptions for user"""
        return UserSubscription.objects.filter(
            user=self.user,
            expiry_date__lte=timezone.now()
        ).select_related('product', 'bundled_plan', 'order')
    
    def get_expiring_soon(self, days=7):
        """Get subscriptions expiring within specified days"""
        expiry_threshold = timezone.now() + timezone.timedelta(days=days)
        return UserSubscription.objects.filter(
            user=self.user,
            status='active',
            is_active=True,
            expiry_date__lte=expiry_threshold,
            expiry_date__gt=timezone.now()
        ).select_related('product', 'bundled_plan', 'order')
    
    def access_product(self, product_slug):
        """
        Record product access and return subscription info
        Returns: (has_access, subscription, message)
        """
        subscription = self.get_subscription_for_product(product_slug)
        
        if not subscription:
            return False, None, "You don't have an active subscription for this product."
        
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
    
    def can_purchase_bundled_plan(self, bundled_plan):
        """
        Check if user can purchase a bundled plan
        Returns: (can_purchase, message)
        """
        if not bundled_plan.is_active:
            return False, "This plan is not available."
        
        # Check max purchases limit
        if bundled_plan.max_purchases_per_user > 0:
            user_purchases = UserSubscription.objects.filter(
                user=self.user,
                bundled_plan=bundled_plan
            ).count()
            
            if user_purchases >= bundled_plan.max_purchases_per_user:
                return False, f"You have reached the maximum purchase limit for this plan."
        
        return True, "You can purchase this plan."
    
    def get_products_with_access(self):
        """Get list of product slugs user has access to"""
        active_subscriptions = self.get_active_subscriptions()
        return [sub.product.slug for sub in active_subscriptions]
    
    def has_purchased_product(self, product_slug):
        """Check if user has ever purchased a product (active or expired)"""
        return UserSubscription.objects.filter(
            user=self.user,
            product__slug=product_slug
        ).exists()


def check_product_access(user, product_slug):
    """
    Decorator helper to check if user has access to a product
    Usage: has_access, subscription, message = check_product_access(request.user, 'jee-counselling')
    """
    manager = SubscriptionManager(user)
    return manager.access_product(product_slug)


def get_user_active_products(user):
    """Get list of all products user has active access to"""
    manager = SubscriptionManager(user)
    return manager.get_products_with_access()


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
    ).select_related('user', 'product')
    
    notifications_sent = 0
    for subscription in expiring_subscriptions:
        # Send email notification
        # send_email_notification(subscription.user, subscription)
        notifications_sent += 1
    
    return notifications_sent


def get_popular_bundled_plans(limit=3):
    """Get popular bundled plans"""
    return BundledPlan.objects.filter(
        is_active=True,
        is_popular=True
    ).order_by('display_order')[:limit]


def get_featured_bundled_plans(limit=6):
    """Get featured bundled plans"""
    return BundledPlan.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('display_order')[:limit]


def get_all_active_bundled_plans():
    """Get all active bundled plans"""
    return BundledPlan.objects.filter(
        is_active=True
    ).prefetch_related('products').order_by('display_order', 'name')


def get_products_by_category(category_slug=None):
    """Get products optionally filtered by category"""
    queryset = MyProducts.objects.filter(is_active=True)
    
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    
    return queryset.order_by('display_order', 'name')


def get_products_by_type(service_type):
    """Get products by type (counselling, predictor, etc.)"""
    return MyProducts.objects.filter(
        is_active=True,
        service_type=service_type
    ).order_by('display_order', 'name')


def get_products_by_exam(exam_type):
    """Get products by exam type"""
    return MyProducts.objects.filter(
        is_active=True,
        exam_type=exam_type
    ).order_by('display_order', 'name')
