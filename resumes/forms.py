from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resume, Education, Experience, Skill


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'email', 'phone', 'address', 'summary']
        
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '123 Main Street, City, State, ZIP'
            }),
            'summary': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write a brief professional summary...'
            }),
        }
        
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address': 'Address/Location',
            'summary': 'Professional Summary',
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_date', 'end_date', 'description']
        
        widgets = {
            'degree': forms.TextInput(attrs={
                'placeholder': 'e.g., Bachelor of Science in Computer Science'
            }),
            'institution': forms.TextInput(attrs={
                'placeholder': 'e.g., Stanford University'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'GPA, honors, relevant coursework...'
            }),
        }
        
        labels = {
            'degree': 'Degree/Certification',
            'institution': 'School/University',
            'start_date': 'Start Date',
            'end_date': 'End Date (leave blank if ongoing)',
            'description': 'Additional Details',
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
        
        widgets = {
            'job_title': forms.TextInput(attrs={
                'placeholder': 'e.g., Senior Software Engineer'
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'e.g., Google Inc.'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your responsibilities and achievements...'
            }),
        }
        
        labels = {
            'job_title': 'Job Title',
            'company': 'Company Name',
            'start_date': 'Start Date',
            'end_date': 'End Date (leave blank if current)',
            'description': 'Job Description',
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Python, Project Management'
            }),
        }
        
        labels = {
            'name': 'Skill Name',
            'proficiency': 'Proficiency Level',
        }