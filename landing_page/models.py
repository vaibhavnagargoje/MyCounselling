from django.db import models
from django.utils import timezone

# Create your models here.

class ContactSubmission(models.Model):
    INQUIRY_CHOICES = [
        ('NEET_UG', 'NEET (UG) Counselling'),
        ('JEE_MAIN_ADV', 'JEE (Main/Advanced) Counselling'),
        ('STATE_CET', 'MHT-CET / KCET / State CET Counselling'),
        ('OTHER_EXAM', 'Other Competitive Exams'),
        ('COUNSELLING_PLANS', 'Counselling Plans & Pricing'),
        ('INSTITUTION_PARTNER', 'Institution Partnership'),
        ('PROMOTION_COLLAB', 'Promotion & Collaboration'),
        ('DOCUMENTATION', 'Documentation Support'),
        ('TECHNICAL_SUPPORT', 'Technical Support'),
        ('GENERAL_INQUIRY', 'General Inquiry'),
        ('OTHER', 'Other'),
    ]
    
    # Basic Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    inquiry_type = models.CharField(max_length=30, choices=INQUIRY_CHOICES, verbose_name='Inquiry Type')
    message = models.TextField()
    
    # Optional Document
    supporting_document = models.FileField(
        upload_to='contact_documents/%Y/%m/',
        blank=True,
        null=True,
        help_text='PDF, JPG, PNG up to 5 MB'
    )
    
    # Metadata
    is_read = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Admin Notes
    admin_notes = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
    
    def __str__(self):
        return f"{self.full_name} - {self.get_inquiry_type_display()} ({self.submitted_at.strftime('%Y-%m-%d')})"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
