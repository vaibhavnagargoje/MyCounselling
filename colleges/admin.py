from django.contrib import admin
from django.utils.html import format_html
from .models import EngineeringCollege, PlacementRecord


class PlacementRecordInline(admin.TabularInline):
    """Inline admin for placement records"""
    model = PlacementRecord
    extra = 1
    fields = ('academic_year', 'placement_percentage', 'students_placed', 'total_students', 
              'highest_package', 'average_package', 'is_verified')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EngineeringCollege)
class EngineeringCollegeAdmin(admin.ModelAdmin):
    """Admin configuration for Engineering College model"""
    
    list_display = ('college_code', 'college_name', 'city', 'state', 'established_year', 
                   'national_ranking', 'is_active', 'is_approved', 'created_at')
    
    list_filter = ('is_active', 'is_approved', 'state', 'established_year', 'created_at')
    
    search_fields = ('college_name', 'college_code', 'city', 'state', 'description')
    
    list_editable = ('is_active', 'is_approved')
    
    readonly_fields = ('created_at', 'updated_at', 'location')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('college_code', 'college_name', 'status', 'description')
        }),
        ('Location Details', {
            'fields': ('address', 'city', 'state', 'country', 'pincode'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('website', 'phone', 'email', 'established_year'),
            'classes': ('collapse',)
        }),
        ('Rankings', {
            'fields': ('national_ranking', 'state_ranking', 'nirf_ranking'),
            'classes': ('collapse',)
        }),
        ('Status & Timestamps', {
            'fields': ('is_active', 'is_approved', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PlacementRecordInline]
    
    list_per_page = 25
    
    ordering = ('college_name',)
    
    actions = ['make_active', 'make_inactive', 'make_approved']
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} colleges were successfully marked as active.')
    make_active.short_description = "Mark selected colleges as active"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} colleges were successfully marked as inactive.')
    make_inactive.short_description = "Mark selected colleges as inactive"
    
    def make_approved(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} colleges were successfully approved.')
    make_approved.short_description = "Mark selected colleges as approved"


@admin.register(PlacementRecord)
class PlacementRecordAdmin(admin.ModelAdmin):
    """Admin configuration for Placement Record model"""
    
    list_display = ('college', 'academic_year', 'placement_percentage', 'students_placed', 
                   'total_students', 'highest_package', 'average_package', 'is_verified')
    
    list_filter = ('academic_year', 'is_verified', 'college__state', 'created_at')
    
    search_fields = ('college__college_name', 'college__college_code', 'academic_year', 'top_recruiters')
    
    list_editable = ('is_verified',)
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('college', 'academic_year', 'is_verified')
        }),
        ('Student Statistics', {
            'fields': ('total_students', 'students_placed', 'placement_percentage')
        }),
        ('Package Details', {
            'fields': ('highest_package', 'average_package', 'median_package')
        }),
        ('Company Information', {
            'fields': ('total_companies_visited', 'top_recruiters')
        }),
        ('Additional Details', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25
    
    ordering = ('-academic_year', 'college__college_name')
    
    autocomplete_fields = ['college']
    
    actions = ['mark_verified', 'mark_unverified']
    
    def mark_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} placement records were successfully marked as verified.')
    mark_verified.short_description = "Mark selected records as verified"
    
    def mark_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} placement records were successfully marked as unverified.')
    mark_unverified.short_description = "Mark selected records as unverified"
