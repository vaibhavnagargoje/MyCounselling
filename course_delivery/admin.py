from django.contrib import admin
from .models import CourseSession, CourseResource, StudentDeliverable

@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'start_time', 'meeting_platform', 'status', 'is_public')
    list_filter = ('meeting_platform', 'start_time', 'is_public', 'product')
    search_fields = ('title', 'product__name', 'description')
    autocomplete_fields = ['product', 'specific_users']
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('Course Info', {
            'fields': ('product', 'title', 'description')
        }),
        ('Schedule', {
            'fields': ('start_time', 'end_time')
        }),
        ('Meeting Details', {
            'fields': ('meeting_platform', 'meeting_link', 'meeting_password', 'recording_url')
        }),
        ('Access Control', {
            'fields': ('is_public', 'specific_users'),
            'description': 'Leave "Specific users" empty to make this session available to ALL enrolled students.'
        }),
    )

@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'resource_type', 'display_order', 'created_at')
    list_filter = ('resource_type', 'product', 'created_at')
    search_fields = ('title', 'product__name', 'content')
    autocomplete_fields = ['product', 'specific_users']
    list_editable = ('display_order',)
    
    fieldsets = (
        ('Resource Info', {
            'fields': ('product', 'title', 'resource_type', 'display_order')
        }),
        ('Content', {
            'fields': ('content', 'video_url', 'file_upload')
        }),
        ('Access Control', {
            'fields': ('is_public', 'specific_users'),
            'description': 'Leave "Specific users" empty to make this resource available to ALL enrolled students.'
        }),
    )

@admin.register(StudentDeliverable)
class StudentDeliverableAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'product', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('title', 'student__username', 'student__email')
    autocomplete_fields = ['student', 'product', 'session']
    
    fieldsets = (
        ('Recipient', {
            'fields': ('student', 'product', 'session')
        }),
          ('File Details', {
        'fields': ('title', 'file_upload', 'remarks')
    }),
    )
