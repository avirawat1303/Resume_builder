from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    """
    Main Resume model - stores basic information about the resume.
    Each user can have multiple resumes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name}'s Resume"


class Education(models.Model):
    """
    Education model - stores educational qualifications.
    Each resume can have multiple education entries.
    """
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='education'
    )
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"


class Experience(models.Model):
    """
    Work Experience model - stores job history.
    Each resume can have multiple work experience entries.
    """
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='experience'
    )
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Skill(models.Model):
    """
    Skills model - stores technical and soft skills.
    Each resume can have multiple skills.
    """
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    name = models.CharField(max_length=100)
    
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    ]
    
    proficiency = models.CharField(
        max_length=50,
        choices=PROFICIENCY_CHOICES
    )
    
    def __str__(self):
        return f"{self.name} ({self.proficiency})"