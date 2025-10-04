from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resume, Education, Experience, Skill

class SignupForm(UserCreationForm):
    
    email=forms.EmailFeild(required=True)
    
    class meta:
        model:User
        fields=['username','email','password1','password2']
        
class ResumeForm(forms.ModelForm):
    class meta:
        model:Resume
        fields=['full_name','email','phone','address','summary']
    
    widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'summary': forms.Textarea(attrs={'rows': 4}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_date', 'end_date', 'description']
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']