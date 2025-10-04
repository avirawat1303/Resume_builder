from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#each user cna have mutiple resumes, i.e many to one realtionship
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    summary = models.TextField(blank=True)
    experience = models.TextField()
    education = models.TextField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  f"{self.full_name}'s Resume"