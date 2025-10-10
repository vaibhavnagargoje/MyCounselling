from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid


class ExamType(models.Model):
    """
    Exam types that can be managed dynamically
    E.g., NEET, JEE, MH-CET, BITSAT, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True, help_text="Short code for the exam (e.g., 'neet', 'jee')")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exam_types'
        verbose_name = 'Exam Type'
        verbose_name_plural = 'Exam Types'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    """
    Categories for different types of services
    E.g., Counselling, College Predictor, Mock Tests, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_categories'
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class Service(models.Model):
    """
    Individual services that can be sold independently or bundled
    E.g., JEE Counselling, NEET Counselling, College Predictor, etc.
    """
    SERVICE_TYPE_CHOICES = [
        ('counselling', 'Counselling'),
        ('predictor', 'College Predictor'),
        ('college_insights', 'College Insights'),
        ('mentorship', 'Mentorship'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name='services')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    exam_type = models.ForeignKey(ExamType, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=300, blank=True)
    
    # Features as JSON field or use separate model for more flexibility
    features = models.JSONField(default=list, help_text="List of service features", blank=True, null=True)
    
    # Pricing (can be overridden in plans)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Service validity
    validity_days = models.IntegerField(default=365, help_text="Number of days the service is valid")
    
    # Media
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='services/thumbnails/', blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['service_type', 'is_active']),
        ]
    
    def __str__(self):
        return self.name


class Plan(models.Model):
    """
    Subscription plans that can bundle multiple services
    E.g., Premium Engineering Package, NEET Complete, Individual Services
    """
    PLAN_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    
    description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=300, blank=True)
    
    # Services included in this plan
    services = models.ManyToManyField(Service, through='PlanService', related_name='plans')
    
    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Plan validity
    validity_days = models.IntegerField(default=365, help_text="Number of days the plan is valid")
    
    # Features and benefits
    features = models.JSONField(default=list, help_text="List of plan features", blank=True, null=True)
    
    # Media
    image = models.ImageField(upload_to='plans/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='plans/thumbnails/', blank=True, null=True)
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    # Limits
    max_purchases_per_user = models.IntegerField(
        default=1,
        help_text="Maximum times a user can purchase this plan. 0 = unlimited"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plans'
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]
    
    def __str__(self):
        return self.name
    
    def calculate_discount(self):
        """Calculate discount percentage"""
        if self.original_price > 0:
            return int(((self.original_price - self.selling_price) / self.original_price) * 100)
        return 0
    
    def save(self, *args, **kwargs):
        # Auto-calculate discount percentage
        if self.original_price and self.selling_price:
            self.discount_percentage = self.calculate_discount()
        super().save(*args, **kwargs)


class PlanService(models.Model):
    """
    Through model for Plan-Service relationship
    Allows customization of service within a plan
    """
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    
    # Custom validity for this service in this plan (optional)
    custom_validity_days = models.IntegerField(
        null=True,
        blank=True,
        help_text="Override service validity for this plan"
    )
    
    # Order in which services are displayed in the plan
    display_order = models.IntegerField(default=0)
    
    # Additional features specific to this service in this plan
    additional_features = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'plan_services'
        verbose_name = 'Plan Service'
        verbose_name_plural = 'Plan Services'
        unique_together = [['plan', 'service']]
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.plan.name} - {self.service.name}"
    
    def get_validity_days(self):
        """Get validity days, using custom if available, otherwise service default"""
        return self.custom_validity_days if self.custom_validity_days else self.service.validity_days


class Order(models.Model):
    """
    Order model to track purchases
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
        ('gpay', 'Google Pay'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Wallet'),
        ('other', 'Other'),
    ]
    
    # Order identification
    order_id = models.CharField(max_length=100, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    
    # What was purchased
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='orders', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='orders', null=True, blank=True)
    
    # Pricing details (store at time of purchase)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Coupon/Promo code
    coupon_code = models.CharField(max_length=50, blank=True)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Tax details
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_gateway_order_id = models.CharField(max_length=200, blank=True)
    payment_gateway_payment_id = models.CharField(max_length=200, blank=True)
    payment_gateway_signature = models.CharField(max_length=500, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_completed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)
    
    def generate_order_id(self):
        """Generate unique order ID"""
        return f"ORD-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    def mark_completed(self):
        """Mark order as completed"""
        self.status = 'completed'
        self.payment_completed_at = timezone.now()
        self.save()
        
        # Create user subscription
        self.create_user_subscription()
    
    def create_user_subscription(self):
        """Create user subscription after successful payment"""
        if self.status == 'completed':
            if self.plan:
                # Create subscriptions for all services in the plan
                for plan_service in self.plan.planservice_set.all():
                    UserSubscription.objects.create(
                        user=self.user,
                        order=self,
                        plan=self.plan,
                        service=plan_service.service,
                        validity_days=plan_service.get_validity_days(),
                        start_date=timezone.now(),
                        expiry_date=timezone.now() + timezone.timedelta(days=plan_service.get_validity_days())
                    )
            elif self.service:
                # Create subscription for individual service
                UserSubscription.objects.create(
                    user=self.user,
                    order=self,
                    service=self.service,
                    validity_days=self.service.validity_days,
                    start_date=timezone.now(),
                    expiry_date=timezone.now() + timezone.timedelta(days=self.service.validity_days)
                )


class UserSubscription(models.Model):
    """
    Track user's active subscriptions and access to services
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
    ]
    
    # User and order info
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='subscriptions')
    
    # What was purchased
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    
    # Validity
    validity_days = models.IntegerField()
    start_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    
    # Usage tracking
    last_accessed = models.DateTimeField(null=True, blank=True)
    access_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_subscriptions'
        verbose_name = 'User Subscription'
        verbose_name_plural = 'User Subscriptions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status', 'is_active']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['service', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.service.name}"
    
    def is_valid(self):
        """Check if subscription is still valid"""
        return (
            self.status == 'active' and
            self.is_active and
            timezone.now() < self.expiry_date
        )
    
    def check_and_update_status(self):
        """Check and update subscription status based on expiry"""
        if self.status == 'active' and timezone.now() >= self.expiry_date:
            self.status = 'expired'
            self.is_active = False
            self.save()
        return self.status
    
    def record_access(self):
        """Record when user accesses the service"""
        self.last_accessed = timezone.now()
        self.access_count += 1
        self.save()
    
    def days_remaining(self):
        """Get days remaining in subscription"""
        if self.expiry_date > timezone.now():
            return (self.expiry_date - timezone.now()).days
        return 0


class Coupon(models.Model):
    """
    Discount coupons for orders
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    
    # Discount details
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum discount amount for percentage coupons"
    )
    
    # Minimum order value
    min_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Usage limits
    max_uses = models.IntegerField(
        default=0,
        help_text="Maximum number of times this coupon can be used. 0 = unlimited"
    )
    max_uses_per_user = models.IntegerField(
        default=1,
        help_text="Maximum times a single user can use this coupon"
    )
    current_uses = models.IntegerField(default=0)
    
    # Applicable to
    applicable_plans = models.ManyToManyField(Plan, blank=True, related_name='coupons')
    applicable_services = models.ManyToManyField(Service, blank=True, related_name='coupons')
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_coupons'
    )
    
    class Meta:
        db_table = 'coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['valid_from', 'valid_until']),
        ]
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        """Check if coupon is valid"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.max_uses == 0 or self.current_uses < self.max_uses)
        )
    
    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount"""
        if not self.is_valid():
            return Decimal('0')
        
        if order_amount < self.min_order_value:
            return Decimal('0')
        
        if self.discount_type == 'percentage':
            discount = (order_amount * self.discount_value) / Decimal('100')
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value
        
        return min(discount, order_amount)


class CouponUsage(models.Model):
    """
    Track coupon usage by users
    """
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='coupon_usage')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'coupon_usages'
        verbose_name = 'Coupon Usage'
        verbose_name_plural = 'Coupon Usages'
        ordering = ['-used_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"
