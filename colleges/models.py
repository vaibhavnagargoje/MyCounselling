from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class EngineeringCollege(models.Model):
    """Main college model with normalized relationships"""
    college_code = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text="Unique college code")
    college_name = models.CharField(max_length=200, null=True, blank=True, help_text="Full name of the college")
    status = models.CharField(max_length=255, null=True, blank=True, help_text="College Status")
    
    # Location details
    city = models.CharField(max_length=100, null=True, blank=True, help_text="City where college is located")
    state = models.CharField(max_length=100, null=True, blank=True, help_text="State where college is located")
    country = models.CharField(max_length=100, default="India", null=True, blank=True, help_text="Country where college is located")
    pincode = models.CharField(max_length=10, blank=True, null=True, help_text="Postal code")
    address = models.TextField(blank=True, null=True, help_text="Complete address")
    
    # Basic details
    established_year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2030)],
        null=True, blank=True,
        help_text="Year of establishment"
    )
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text="Brief description of the college")
    
    
    # Rankings and ratings
    national_ranking = models.IntegerField(blank=True, null=True, help_text="National ranking")
    state_ranking = models.IntegerField(blank=True, null=True, help_text="State ranking")
    nirf_ranking = models.IntegerField(blank=True, null=True, help_text="NIRF ranking")
    
    # Status
    is_active = models.BooleanField(default=True, null=True, blank=True, help_text="Whether this college is currently active")
    is_approved = models.BooleanField(default=False, null=True, blank=True, help_text="Whether this college is approved by authorities")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['college_name']
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
        unique_together = ['college_name', 'city', 'state']
    
    def __str__(self):
        return f"{self.college_code} - {self.college_name}"
    
    @property
    def location(self):
        """Return formatted location"""
        return f"{self.city}, {self.state}"
    
    @property
    def latest_placement(self):
        """Return the latest placement record"""
        return self.placement_records.order_by('-academic_year').first()

    def get_fee_range(self):
        """Return formatted fee range"""
        if self.fees_range_min and self.fees_range_max:
            return f"₹{self.fees_range_min:,.0f} - ₹{self.fees_range_max:,.0f}"
        elif self.fees_range_min:
            return f"₹{self.fees_range_min:,.0f}+"
        return "Not specified"




class PlacementRecord(models.Model):
    """Model to store placement records for colleges"""
    college = models.ForeignKey(EngineeringCollege, on_delete=models.CASCADE, related_name='placement_records', null=True, blank=True)
    academic_year = models.CharField(max_length=20, null=True, blank=True, help_text="Academic year (e.g., 2023-24)")
    
    # Placement statistics
    total_students = models.IntegerField(null=True, blank=True, help_text="Total number of eligible students")
    students_placed = models.IntegerField(null=True, blank=True, help_text="Number of students placed")
    placement_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Placement percentage")
    
    # Package details
    highest_package = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Highest package offered (in LPA)")
    average_package = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Average package (in LPA)")
    median_package = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Median package (in LPA)")
    
    # Company details
    total_companies_visited = models.IntegerField(default=0, null=True, blank=True, help_text="Total number of companies visited")
    top_recruiters = models.TextField(blank=True, null=True, help_text="Comma-separated list of top recruiters")
    
    # Additional details
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about placements")
    is_verified = models.BooleanField(default=False, null=True, blank=True, help_text="Whether this data is verified")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-academic_year']
        unique_together = ['college', 'academic_year']
        verbose_name = 'Placement Record'
        verbose_name_plural = 'Placement Records'
    
    def __str__(self):
        return f"{self.college.college_name} - {self.academic_year} ({self.placement_percentage}%)"
    
    def get_top_recruiters_list(self):
        """Return top recruiters as a list"""
        if self.top_recruiters:
            return [recruiter.strip() for recruiter in self.top_recruiters.split(',')]
        return []


