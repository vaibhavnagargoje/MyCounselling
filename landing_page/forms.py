from django import forms
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['full_name', 'email', 'phone', 'inquiry_type', 'message', 'supporting_document']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'input-primary',
                'placeholder': 'Enter your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-primary',
                'placeholder': 'you@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input-primary',
                'placeholder': '+91-98765 43210'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'input-primary'
            }),
            'message': forms.Textarea(attrs={
                'class': 'input-primary resize-none',
                'rows': 5,
                'placeholder': 'Tell us about your query, preferred plan, or exam details'
            }),
            'supporting_document': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }
    
    def clean_supporting_document(self):
        file = self.cleaned_data.get('supporting_document')
        if file:
            # Check file size (5 MB limit)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 5 MB.')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
            ext = file.name.lower().split('.')[-1]
            if f'.{ext}' not in allowed_extensions:
                raise forms.ValidationError('Only PDF, JPG, and PNG files are allowed.')
        
        return file
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Remove common separators
        phone = phone.replace('-', '').replace(' ', '').replace('+', '')
        
        # Basic validation for Indian phone numbers
        if not phone.isdigit() or len(phone) < 10:
            raise forms.ValidationError('Please enter a valid phone number.')
        
        return phone
