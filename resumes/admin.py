from django.contrib import admin

# Register your models here.
from .models import Resume , Education, Experience, Skill
admin .site.register(Resume)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)

