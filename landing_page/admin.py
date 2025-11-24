from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ContactSubmission
import os

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'inquiry_type', 'is_read', 'has_document', 'submitted_at']
    list_filter = ['is_read', 'inquiry_type', 'submitted_at']
    search_fields = ['full_name', 'email', 'phone', 'message', 'admin_notes']
    readonly_fields = ['submitted_at', 'updated_at', 'ip_address', 'user_agent', 'document_preview']
    list_editable = ['is_read']
    date_hierarchy = 'submitted_at'
    
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
