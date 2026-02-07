from django import forms
from .models import ContactSubmission, ConsultationRequest


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = [
            'full_name', 'email', 'phone', 'city', 'state',
            'exam_appeared', 'rank_or_score', 'preferred_stream',
            'preferred_colleges', 'budget_range', 'special_requirements',
            'urgency', 'supporting_document'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm',
                'placeholder': 'e.g. Rahul Sharma'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm',
                'placeholder': 'you@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm',
                'placeholder': '+91-98765 43210'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm',
                'placeholder': 'e.g. Pune'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm',
                'placeholder': 'e.g. Maharashtra'
            }),
            'exam_appeared': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm'
            }),
            'rank_or_score': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm',
                'placeholder': 'e.g. Rank 45000 or 85 percentile'
            }),
            'preferred_stream': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm'
            }),
            'preferred_colleges': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm resize-none',
                'rows': 2,
                'placeholder': 'e.g. COEP Pune, VIT Vellore, NIT Surathkal (optional)'
            }),
            'budget_range': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm resize-none',
                'rows': 4,
                'placeholder': 'Describe your specific need — e.g. lateral entry guidance, NRI quota, management seat, domicile issues, special category reservation, etc.'
            }),
            'urgency': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm'
            }),
            'supporting_document': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition cursor-pointer',
                'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx'
            })
        }
    
    def clean_supporting_document(self):
        file = self.cleaned_data.get('supporting_document')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 10 MB.')
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
            ext = '.' + file.name.lower().rsplit('.', 1)[-1]
            if ext not in allowed_extensions:
                raise forms.ValidationError('Only PDF, JPG, PNG, DOC, DOCX files are allowed.')
        return file
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        cleaned = phone.replace('-', '').replace(' ', '').replace('+', '')
        if not cleaned.isdigit() or len(cleaned) < 10:
            raise forms.ValidationError('Please enter a valid phone number.')
        return phone


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
