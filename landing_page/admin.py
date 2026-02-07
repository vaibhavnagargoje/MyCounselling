from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ContactSubmission, ConsultationRequest
import os


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'exam_appeared', 'preferred_stream', 'urgency', 'status', 'is_read', 'has_document', 'submitted_date']
    list_filter = ['status', 'is_read', 'exam_appeared', 'preferred_stream', 'urgency', 'budget_range']
    search_fields = ['full_name', 'email', 'phone', 'city', 'state', 'rank_or_score', 'special_requirements', 'admin_notes']
    readonly_fields = ['submitted_at', 'updated_at', 'ip_address', 'user_agent', 'document_preview']
    list_editable = ['status', 'is_read']
    list_per_page = 25
    
    def submitted_date(self, obj):
        """Display submitted date without timezone conversion issues"""
        return obj.submitted_at.strftime('%d %b %Y, %I:%M %p') if obj.submitted_at else '-'
    submitted_date.short_description = 'Submitted'
    submitted_date.admin_order_field = 'submitted_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone', 'city', 'state')
        }),
        ('Academic Details', {
            'fields': ('exam_appeared', 'rank_or_score', 'preferred_stream', 'preferred_colleges')
        }),
        ('Requirements', {
            'fields': ('budget_range', 'special_requirements', 'urgency')
        }),
        ('Document', {
            'fields': ('supporting_document', 'document_preview')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'is_read', 'assigned_to', 'follow_up_date', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'updated_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_in_progress', 'mark_resolved']
    
    def has_document(self, obj):
        if obj.supporting_document:
            return format_html('<span style="color: green;">\u2713</span>')
        return format_html('<span style="color: red;">\u2717</span>')
    has_document.short_description = 'Doc'
    
    def document_preview(self, obj):
        if not obj.supporting_document:
            return format_html('<p style="color: gray;">No document uploaded</p>')
        file_url = obj.supporting_document.url
        file_name = os.path.basename(obj.supporting_document.name)
        file_ext = os.path.splitext(file_name)[1].lower()
        if file_ext in ['.jpg', '.jpeg', '.png']:
            return format_html(
                '<div><p><strong>File:</strong> {}</p>'
                '<a href="{}" target="_blank"><img src="{}" style="max-width:400px;max-height:400px;border:1px solid #ddd;border-radius:4px;padding:5px;"/></a>'
                '<p><a href="{}" target="_blank" class="button">Download</a></p></div>',
                file_name, file_url, file_url, file_url
            )
        return format_html(
            '<div><p><strong>File:</strong> {}</p>'
            '<p><a href="{}" target="_blank" class="button">Download File</a></p></div>',
            file_name, file_url
        )
    document_preview.short_description = 'Document Preview'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} request(s) marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='IN_PROGRESS')
        self.message_user(request, f'{updated} request(s) marked as In Progress.')
    mark_in_progress.short_description = 'Mark as In Progress'
    
    def mark_resolved(self, request, queryset):
        updated = queryset.update(status='RESOLVED')
        self.message_user(request, f'{updated} request(s) marked as Resolved.')
    mark_resolved.short_description = 'Mark as Resolved'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['full_name', 'email', 'phone', 'city', 'state',
                                           'exam_appeared', 'rank_or_score', 'preferred_stream',
                                           'preferred_colleges', 'budget_range', 'special_requirements',
                                           'urgency', 'supporting_document']
        return self.readonly_fields


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'inquiry_type', 'is_read', 'has_document', 'submitted_date']
    list_filter = ['is_read', 'inquiry_type']
    search_fields = ['full_name', 'email', 'phone', 'message', 'admin_notes']
    readonly_fields = ['submitted_at', 'updated_at', 'ip_address', 'user_agent', 'document_preview']
    list_editable = ['is_read']
    
    def submitted_date(self, obj):
        """Display submitted date without timezone conversion issues"""
        return obj.submitted_at.strftime('%d %b %Y, %I:%M %p') if obj.submitted_at else '-'
    submitted_date.short_description = 'Submitted'
    submitted_date.admin_order_field = 'submitted_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone', 'inquiry_type')
        }),
        ('Message', {
            'fields': ('message', 'supporting_document', 'document_preview')
        }),
        ('Status & Assignment', {
            'fields': ('is_read', 'assigned_to', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'updated_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def has_document(self, obj):
        """Display if document is attached"""
        if obj.supporting_document:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    has_document.short_description = 'Document'
    
    def document_preview(self, obj):
        """Display preview of uploaded document"""
        if not obj.supporting_document:
            return format_html('<p style="color: gray;">No document uploaded</p>')
        
        file_url = obj.supporting_document.url
        file_name = os.path.basename(obj.supporting_document.name)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # Display image preview for image files
        if file_ext in ['.jpg', '.jpeg', '.png']:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>File:</strong> {}</p>'
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width: 400px; max-height: 400px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;"/>'
                '</a>'
                '<p><a href="{}" target="_blank" class="button">Download File</a></p>'
                '</div>',
                file_name, file_url, file_url, file_url
            )
        
        # Display link for PDF files
        elif file_ext == '.pdf':
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>File:</strong> {}</p>'
                '<iframe src="{}" style="width: 100%; height: 500px; border: 1px solid #ddd;"></iframe>'
                '<p><a href="{}" target="_blank" class="button">Download PDF</a></p>'
                '</div>',
                file_name, file_url, file_url
            )
        
        # Generic download link for other files
        else:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>File:</strong> {}</p>'
                '<p><a href="{}" target="_blank" class="button">Download File</a></p>'
                '</div>',
                file_name, file_url
            )
    
    document_preview.short_description = 'Document Preview'
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} submission(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} submission(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected as unread'
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly when editing existing object"""
        if obj:  # Editing existing object
            return self.readonly_fields + ['full_name', 'email', 'phone', 'inquiry_type', 'message', 'supporting_document']
        return self.readonly_fields
