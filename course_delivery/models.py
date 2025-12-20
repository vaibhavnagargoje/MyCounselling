from django.db import models
from django.contrib.auth.models import User
from products.models import MyProducts

class CourseSession(models.Model):
    """
    Represents a LIVE class/session (Zoom, Meet, etc.)
    """
    PLATFORM_CHOICES = [
        ('zoom', 'Zoom'),
        ('meet', 'Google Meet'),
        ('teams', 'Microsoft Teams'),
        ('other', 'Other'),
    ]

    # Link to the product (Course)
    product = models.ForeignKey(MyProducts, on_delete=models.CASCADE, related_name='course_sessions')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Scheduling
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    # Session Details
    meeting_platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='zoom')
    meeting_link = models.URLField(help_text="The join link for the student")
    meeting_password = models.CharField(max_length=50, blank=True, help_text="Optional meeting password")
    
    # Post-session
    recording_url = models.URLField(blank=True, null=True, help_text="Link to watch the replay")

    # --- ACCESS CONTROL LOGIC ---
    is_public = models.BooleanField(default=False, help_text="If checked, ANYONE can see this (even non-enrolled).")
    
    # If this is empty, we assume ALL enrolled students can see it.
    # If users are selected here, ONLY these specific users can see it.
    specific_users = models.ManyToManyField(
        User, 
        blank=True, 
        related_name='special_sessions',
        help_text="Select users ONLY for 1-on-1 or special group sessions. Leave empty for all enrolled students."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']
        verbose_name = "Live Session"

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%d %b %H:%M')}"

    @property
    def status(self):
        from django.utils import timezone
        now = timezone.now()
        if now < self.start_time:
            return "Upcoming"
        elif self.start_time <= now <= self.end_time:
            return "Live"
        else:
            return "Completed"


class CourseResource(models.Model):
    """
    Represents Static Content (Instructions, Videos, PDFs)
    """
    TYPE_CHOICES = [
        ('video', 'Video'),
        ('instruction', 'Text Instruction/Note'),
        ('document', 'PDF/File'),
    ]

    product = models.ForeignKey(MyProducts, on_delete=models.CASCADE, related_name='course_resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='instruction')
    
    # Content
    content = models.TextField(blank=True, help_text="Main text content or description")
    video_url = models.URLField(blank=True, null=True, help_text="YouTube/Vimeo/S3 link")
    file_upload = models.FileField(upload_to='course_materials/', blank=True, null=True)
    
    # --- ACCESS CONTROL LOGIC ---
    is_public = models.BooleanField(default=False)
    
    # Same logic: Empty = All Enrolled, Populated = Restricted
    specific_users = models.ManyToManyField(
        User, 
        blank=True, 
        related_name='special_resources',
        help_text="Limit visibility to specific users only."
    )

    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()})"


class StudentDeliverable(models.Model):
    """
    Represents a file specifically uploaded for ONE student.
    E.g., A personalized report card, a counselling summary, or a specific homework file.
    """
    # Link to the specific student (Required)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_deliverables')
    
    # Link to the course (Required - so we know which dashboard to show it on)
    product = models.ForeignKey(MyProducts, on_delete=models.CASCADE, related_name='student_deliverables')
    
    # Optional: Link to a specific session (if this file is a result of that session)
    session = models.ForeignKey(CourseSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliverables')
    
    title = models.CharField(max_length=200, help_text="E.g., 'Your Counselling Report - 20th Dec'")
    file_upload = models.FileField(upload_to='student_specific_files/%Y/%m/')
    remarks = models.TextField(blank=True, help_text="Private note for the student regarding this file")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Student Specific File"
        verbose_name_plural = "Student Specific Files"
        ordering = ['-created_at']

    def __str__(self):
        return f"File for {self.student.username}: {self.title}"
