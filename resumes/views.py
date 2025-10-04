from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .forms import SignUpForm, ResumeForm, EducationForm, ExperienceForm, SkillForm
from .models import Resume, Education, Experience, Skill

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def home(request):
    return render(request, 'resumes/home.html')

def signup(request):
   
    if request.method == 'POST':
        # Form submitted
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          # Create user in database
            login(request, user)        # Log them in automatically
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'resumes/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Credentials correct
            login(request, user)
            return redirect('dashboard')
        else:
            # Wrong username or password
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'resumes/login.html')

@login_required
def user_logout(request):
    
    logout(request)  # Destroys session
    return redirect('home')


@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/dashboard.html', {'resumes': resumes})

@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)  # Don't save yet
            resume.user = request.user        # Set the user
            resume.save()                     # Now save
            messages.success(request, 'Resume created successfully!')
            return redirect('edit_resume', resume_id=resume.id)
    else:
        form = ResumeForm()
    
    return render(request, 'resumes/create_resume.html', {'form': form})

@login_required
def edit_resume(request, resume_id):
    # Get resume or show 404 if not found
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume updated successfully!')
            return redirect('edit_resume', resume_id=resume.id)
    else:
        form = ResumeForm(instance=resume)
    
    context = {
        'resume': resume,
        'form': form,
        'education_form': EducationForm(),
        'experience_form': ExperienceForm(),
        'skill_form': SkillForm(),
    }
    return render(request, 'resumes/edit_resume.html', context)

@login_required
def add_education(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.resume = resume  # Link to this resume
            education.save()
            messages.success(request, 'Education added!')
    
    return redirect('edit_resume', resume_id=resume.id)

@login_required
def add_experience(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.resume = resume
            experience.save()
            messages.success(request, 'Experience added!')
    
    return redirect('edit_resume', resume_id=resume.id)

@login_required
def add_skill(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            messages.success(request, 'Skill added!')
    
    return redirect('edit_resume', resume_id=resume.id)

@login_required
def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Create PDF in memory (not on disk)
    buffer = BytesIO()
    
    # Create PDF canvas
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # Letter size: 8.5" x 11"
    
    # Starting Y position (top of page)
    y = height - 50
    
    # ========== HEADER ==========
    p.setFont("Helvetica-Bold", 24)
    p.drawString(50, y, resume.full_name)
    
    y -= 20
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"{resume.email} | {resume.phone}")
    
    y -= 15
    p.drawString(50, y, resume.address)
    
    # ========== SUMMARY ==========
    if resume.summary:
        y -= 30
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Professional Summary")
        
        y -= 20
        p.setFont("Helvetica", 11)
        # Simple text wrapping
        text = p.beginText(50, y)
        for line in resume.summary.split('\n'):
            text.textLine(line)
        p.drawText(text)
        y = text.getY() - 10
    
    # ========== EDUCATION ==========
    if resume.education.exists():
        y -= 20
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Education")
        y -= 20
        
        for edu in resume.education.all():
            p.setFont("Helvetica-Bold", 11)
            p.drawString(50, y, edu.degree)
            y -= 15
            
            p.setFont("Helvetica", 10)
            p.drawString(50, y, f"{edu.institution} | {edu.start_date} - {edu.end_date or 'Present'}")
            y -= 20
    
    # ========== EXPERIENCE ==========
    if resume.experience.exists():
        y -= 10
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Experience")
        y -= 20
        
        for exp in resume.experience.all():
            p.setFont("Helvetica-Bold", 11)
            p.drawString(50, y, exp.job_title)
            y -= 15
            
            p.setFont("Helvetica", 10)
            p.drawString(50, y, f"{exp.company} | {exp.start_date} - {exp.end_date or 'Present'}")
            y -= 20
    
    # ========== SKILLS ==========
    if resume.skills.exists():
        y -= 10
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Skills")
        y -= 20
        
        p.setFont("Helvetica", 11)
        skills_text = ", ".join([f"{skill.name} ({skill.proficiency})" for skill in resume.skills.all()])
        p.drawString(50, y, skills_text)
    
    # Finish PDF
    p.showPage()
    p.save()
    
    # Get PDF from memory
    buffer.seek(0)
    
    # Create HTTP response with PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'
    
    return response

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    resume.delete()
    messages.success(request, 'Resume deleted successfully!')
    return redirect('dashboard')