from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# Create your models here.


class ConsultationRequest(models.Model):
    """Model for students who have special/particular requirements and need custom consultation."""
    
    EXAM_CHOICES = [
        ('NEET_UG', 'NEET UG'),
        ('NEET_PG', 'NEET PG'),
        ('JEE_MAIN', 'JEE Main'),
        ('JEE_ADV', 'JEE Advanced'),
        ('MHT_CET', 'MHT-CET'),
        ('KCET', 'KCET'),
        ('STATE_CET', 'Other State CET'),
        ('CUET', 'CUET'),
        ('OTHER', 'Other'),
    ]
    
    BUDGET_CHOICES = [
        ('BELOW_5L', 'Below ₹5 Lakh/year'),
        ('5L_10L', '₹5 – ₹10 Lakh/year'),
        ('10L_15L', '₹10 – ₹15 Lakh/year'),
        ('15L_25L', '₹15 – ₹25 Lakh/year'),
        ('ABOVE_25L', 'Above ₹25 Lakh/year'),
        ('FLEXIBLE', 'Flexible / Not Sure'),
    ]
    
    PREFERRED_STREAM_CHOICES = [
        ('ENGINEERING', 'Engineering / B.Tech'),
        ('MEDICAL', 'Medical / MBBS / BDS'),
        ('PHARMACY', 'Pharmacy'),
        ('ARCHITECTURE', 'Architecture'),
        ('MANAGEMENT', 'Management / MBA'),
        ('LAW', 'Law'),
        ('OTHER', 'Other'),
    ]
    
    URGENCY_CHOICES = [
        ('IMMEDIATE', 'Immediate – Counselling round ongoing'),
        ('THIS_WEEK', 'Within this week'),
        ('THIS_MONTH', 'Within this month'),
        ('EXPLORING', 'Just exploring options'),
    ]
    
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('CONTACTED', 'Contacted'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    
    # Personal Information
    full_name = models.CharField(max_length=200, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email Address')
    phone = models.CharField(max_length=20, verbose_name='Phone Number')
    city = models.CharField(max_length=100, verbose_name='City / District')
    state = models.CharField(max_length=100, verbose_name='State')
    
    # Academic Information
    exam_appeared = models.CharField(max_length=20, choices=EXAM_CHOICES, verbose_name='Exam Appeared For')
    rank_or_score = models.CharField(max_length=50, verbose_name='Rank / Score / Percentile')
    preferred_stream = models.CharField(max_length=20, choices=PREFERRED_STREAM_CHOICES, verbose_name='Preferred Stream')
    preferred_colleges = models.TextField(
        blank=True, null=True,
        verbose_name='Preferred Colleges (if any)',
        help_text='List any specific colleges you are targeting'
    )
    
    # Requirements
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, verbose_name='Budget Range')
    special_requirements = models.TextField(
        verbose_name='Describe Your Specific Requirement',
        help_text='Tell us in detail what help you need — e.g. lateral entry, NRI quota, management seat, domicile issue, category-based queries, etc.'
    )
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, verbose_name='How Urgent Is This?')
    
    # File Upload
    supporting_document = models.FileField(
        upload_to='consultation_documents/%Y/%m/',
        blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])],
        verbose_name='Upload Supporting Document',
        help_text='Scorecard, admit card, category certificate, etc. (PDF, JPG, PNG, DOC — max 10 MB)'
    )
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name='Status')
    is_read = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Admin
    admin_notes = models.TextField(blank=True, null=True, verbose_name='Internal Notes')
    assigned_to = models.CharField(max_length=100, blank=True, null=True, verbose_name='Assigned Counsellor')
    follow_up_date = models.DateField(blank=True, null=True, verbose_name='Follow-up Date')
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Consultation Request'
        verbose_name_plural = 'Consultation Requests'
    
    def __str__(self):
        return f"{self.full_name} – {self.get_exam_appeared_display()} ({self.submitted_at.strftime('%d %b %Y')})"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()


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
