from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ExamType, ServiceCategory, Service, Plan, PlanService,
    Order, UserSubscription, Coupon, CouponUsage
)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'display_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Status', {
            'fields': ('is_active', 'display_order')
        }),
    )


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'display_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'service_type', 'exam_type',
        'base_price', 'validity_days', 'is_active', 'is_featured'
    ]
    list_filter = ['category', 'service_type', 'exam_type', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'service_type', 'exam_type')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'features')
        }),
        ('Pricing & Validity', {
            'fields': ('base_price', 'validity_days')
        }),
        ('Media', {
            'fields': ('image', 'thumbnail')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'display_order')
        }),
    )


class PlanServiceInline(admin.TabularInline):
    model = PlanService
    extra = 1
    fields = ['service', 'custom_validity_days', 'display_order']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'plan_type', 'selling_price', 'original_price',
        'discount_percentage', 'is_active', 'is_popular', 'is_featured'
    ]
    list_filter = ['plan_type', 'is_active', 'is_popular', 'is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PlanServiceInline]
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'plan_type')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'features')
        }),
        ('Pricing', {
            'fields': ('original_price', 'selling_price', 'discount_percentage')
        }),
        ('Validity & Limits', {
            'fields': ('validity_days', 'max_purchases_per_user')
        }),
        ('Media', {
            'fields': ('image', 'thumbnail')
        }),
        ('Status', {
            'fields': ('is_active', 'is_popular', 'is_featured', 'display_order')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['discount_percentage']
        return []


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id', 'user', 'get_product', 'final_price',
        'status', 'payment_method', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = [
        'order_id', 'user__username', 'user__email',
        'payment_gateway_order_id', 'payment_gateway_payment_id'
    ]
    readonly_fields = [
        'order_id', 'created_at', 'updated_at', 'payment_completed_at'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'user', 'plan', 'service')
        }),
        ('Pricing Details', {
            'fields': (
                'original_price', 'discount_amount', 'coupon_code',
                'coupon_discount', 'tax_amount', 'final_price'
            )
        }),
        ('Payment Details', {
            'fields': (
                'payment_method', 'payment_gateway_order_id',
                'payment_gateway_payment_id', 'payment_gateway_signature'
            )
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'ip_address')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'payment_completed_at')
        }),
    )
    
    def get_product(self, obj):
        if obj.plan:
            return format_html('<span style="color: blue;">📦 {}</span>', obj.plan.name)
        elif obj.service:
            return format_html('<span style="color: green;">🎯 {}</span>', obj.service.name)
        return '-'
    get_product.short_description = 'Product'
    
    actions = ['mark_as_completed', 'mark_as_failed', 'mark_as_cancelled']
    
    def mark_as_completed(self, request, queryset):
        for order in queryset:
            order.mark_completed()
        self.message_user(request, f"{queryset.count()} orders marked as completed.")
    mark_as_completed.short_description = "Mark selected orders as completed"
    
    def mark_as_failed(self, request, queryset):
        queryset.update(status='failed')
        self.message_user(request, f"{queryset.count()} orders marked as failed.")
    mark_as_failed.short_description = "Mark selected orders as failed"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} orders marked as cancelled.")
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'service', 'get_plan', 'status',
        'start_date', 'expiry_date', 'days_remaining_display', 'is_active'
    ]
    list_filter = ['status', 'is_active', 'service__category', 'created_at']
    search_fields = ['user__username', 'user__email', 'service__name']
    readonly_fields = [
        'created_at', 'updated_at', 'last_accessed',
        'access_count', 'days_remaining_display'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('User & Product', {
            'fields': ('user', 'order', 'plan', 'service')
        }),
        ('Validity', {
            'fields': (
                'validity_days', 'start_date', 'expiry_date',
                'days_remaining_display'
            )
        }),
        ('Status', {
            'fields': ('status', 'is_active')
        }),
        ('Usage Tracking', {
            'fields': ('last_accessed', 'access_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_plan(self, obj):
        return obj.plan.name if obj.plan else '-'
    get_plan.short_description = 'Plan'
    
    def days_remaining_display(self, obj):
        days = obj.days_remaining()
        if days > 0:
            color = 'green' if days > 30 else 'orange' if days > 7 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{} days</span>',
                color, days
            )
        return format_html('<span style="color: red;">Expired</span>')
    days_remaining_display.short_description = 'Days Remaining'
    
    actions = ['check_and_update_status', 'mark_as_cancelled']
    
    def check_and_update_status(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.check_and_update_status()
            count += 1
        self.message_user(request, f"{count} subscriptions checked and updated.")
    check_and_update_status.short_description = "Check and update subscription status"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled', is_active=False)
        self.message_user(request, f"{queryset.count()} subscriptions cancelled.")
    mark_as_cancelled.short_description = "Cancel selected subscriptions"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'discount_type', 'discount_value',
        'usage_display', 'valid_from', 'valid_until', 'is_active'
    ]
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    filter_horizontal = ['applicable_plans', 'applicable_services']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'description')
        }),
        ('Discount Details', {
            'fields': (
                'discount_type', 'discount_value',
                'max_discount_amount', 'min_order_value'
            )
        }),
        ('Usage Limits', {
            'fields': (
                'max_uses', 'max_uses_per_user', 'current_uses'
            )
        }),
        ('Applicability', {
            'fields': ('applicable_plans', 'applicable_services')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'is_active')
        }),
    )
    
    readonly_fields = ['current_uses']
    
    def usage_display(self, obj):
        if obj.max_uses > 0:
            percentage = (obj.current_uses / obj.max_uses) * 100
            color = 'green' if percentage < 70 else 'orange' if percentage < 90 else 'red'
            return format_html(
                '<span style="color: {};">{} / {}</span>',
                color, obj.current_uses, obj.max_uses
            )
        return format_html('{} / Unlimited', obj.current_uses)
    usage_display.short_description = 'Usage'


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'order', 'discount_amount', 'used_at']
    list_filter = ['used_at', 'coupon']
    search_fields = ['user__username', 'user__email', 'coupon__code', 'order__order_id']
    readonly_fields = ['used_at']
    ordering = ['-used_at']
