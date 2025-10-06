from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .forms import SignUpForm, ResumeForm, EducationForm, ExperienceForm, SkillForm
from .models import Resume, Education, Experience, Skill

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from io import BytesIO


def home(request):
    return render(request, 'resumes/home.html')

def signup(request):
   
    if request.method == 'POST':
        # Form submitted
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          
            login(request, user)       
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    
    return render(request, 'resumes/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
      
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            return redirect('dashboard')
        else:
        
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'resumes/login.html')

@login_required
def user_logout(request):
    
    logout(request)  
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
            resume = form.save(commit=False)  
            resume.user = request.user        
            resume.save()                     
            messages.success(request, 'Resume created successfully!')
            return redirect('edit_resume', resume_id=resume.id)
    else:
        form = ResumeForm()
    
    return render(request, 'resumes/create_resume.html', {'form': form})

@login_required
def edit_resume(request, resume_id):
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
    """
    Generate a professional PDF resume
    """
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Create PDF in memory
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Define colors
    primary_color = colors.HexColor('#2c3e50')
    accent_color = colors.HexColor('#00d9ff')
    text_color = colors.HexColor('#4a5568')
    
    y = height - 50  # Start position from top
    
    # ==================== HEADER SECTION ====================
    # Name
    p.setFont("Helvetica-Bold", 28)
    p.setFillColor(primary_color)
    p.drawCentredString(width/2, y, resume.full_name.upper())
    
    # Contact Information
    y -= 25
    p.setFont("Helvetica", 11)
    p.setFillColor(text_color)
    contact_line = f"{resume.email}  •  {resume.phone}  •  {resume.address}"
    p.drawCentredString(width/2, y, contact_line)
    
    # Horizontal line under header
    y -= 15
    p.setStrokeColor(accent_color)
    p.setLineWidth(2)
    p.line(50, y, width-50, y)
    
    y -= 35
    
    # ==================== PROFESSIONAL SUMMARY ====================
    if resume.summary:
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(accent_color)
        p.drawString(50, y, "PROFESSIONAL SUMMARY")
        
        y -= 5
        p.setStrokeColor(accent_color)
        p.setLineWidth(1)
        p.line(50, y, 235, y)
        
        y -= 20
        p.setFont("Helvetica", 10)
        p.setFillColor(text_color)
        
        # Word wrap for summary
        max_width = width - 100
        words = resume.summary.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if p.stringWidth(test_line, "Helvetica", 10) > max_width:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for line in lines:
            p.drawString(50, y, line)
            y -= 15
        
        y -= 10
    
    # ==================== WORK EXPERIENCE ====================
    if resume.experience.exists():
        if y < 150:
            p.showPage()
            y = height - 50
        
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(accent_color)
        p.drawString(50, y, "WORK EXPERIENCE")
        
        y -= 5
        p.setStrokeColor(accent_color)
        p.setLineWidth(1)
        p.line(50, y, 190, y)
        
        y -= 25
        
        for exp in resume.experience.all():
            if y < 100:
                p.showPage()
                y = height - 50
            
            # Job Title
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(primary_color)
            p.drawString(50, y, exp.job_title)
            
            # Date (right aligned)
            p.setFont("Helvetica", 10)
            p.setFillColor(text_color)
            date_str = f"{exp.start_date.strftime('%b %Y')} - {exp.end_date.strftime('%b %Y') if exp.end_date else 'Present'}"
            date_width = p.stringWidth(date_str, "Helvetica", 10)
            p.drawString(width - 50 - date_width, y, date_str)
            
            y -= 15
            
            # Company
            p.setFont("Helvetica-Oblique", 11)
            p.setFillColor(text_color)
            p.drawString(50, y, exp.company)
            
            y -= 18
            
            # Description with bullet points
            p.setFont("Helvetica", 10)
            desc_lines = exp.description.split('\n')
            
            for line in desc_lines:
                if line.strip():
                    # Check if line starts with bullet
                    if line.strip().startswith('•') or line.strip().startswith('-'):
                        display_line = '  ' + line.strip()
                    else:
                        display_line = '  • ' + line.strip()
                    
                    # Word wrap if needed
                    max_width = width - 120
                    if p.stringWidth(display_line, "Helvetica", 10) > max_width:
                        words = display_line.split()
                        current_line = []
                        for word in words:
                            current_line.append(word)
                            test_line = ' '.join(current_line)
                            if p.stringWidth(test_line, "Helvetica", 10) > max_width:
                                current_line.pop()
                                p.drawString(60, y, ' '.join(current_line))
                                y -= 12
                                current_line = [word]
                        if current_line:
                            p.drawString(60, y, ' '.join(current_line))
                            y -= 12
                    else:
                        p.drawString(60, y, display_line)
                        y -= 12
            
            y -= 15
    
    # ==================== EDUCATION ====================
    if resume.education.exists():
        if y < 150:
            p.showPage()
            y = height - 50
        
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(accent_color)
        p.drawString(50, y, "EDUCATION")
        
        y -= 5
        p.setStrokeColor(accent_color)
        p.setLineWidth(1)
        p.line(50, y, 135, y)
        
        y -= 25
        
        for edu in resume.education.all():
            if y < 100:
                p.showPage()
                y = height - 50
            
            # Degree
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(primary_color)
            p.drawString(50, y, edu.degree)
            
            # Date (right aligned)
            p.setFont("Helvetica", 10)
            p.setFillColor(text_color)
            date_str = f"{edu.start_date.strftime('%b %Y')} - {edu.end_date.strftime('%b %Y') if edu.end_date else 'Present'}"
            date_width = p.stringWidth(date_str, "Helvetica", 10)
            p.drawString(width - 50 - date_width, y, date_str)
            
            y -= 15
            
            # Institution
            p.setFont("Helvetica-Oblique", 11)
            p.drawString(50, y, edu.institution)
            
            y -= 15
            
            # Description if exists
            if edu.description:
                p.setFont("Helvetica", 10)
                desc_lines = edu.description.split('\n')
                for line in desc_lines[:3]:  # Limit to 3 lines
                    if line.strip():
                        p.drawString(60, y, line.strip()[:80])
                        y -= 12
            
            y -= 15
    
    # ==================== SKILLS ====================
    if resume.skills.exists():
        if y < 150:
            p.showPage()
            y = height - 50
        
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(accent_color)
        p.drawString(50, y, "SKILLS")
        
        y -= 5
        p.setStrokeColor(accent_color)
        p.setLineWidth(1)
        p.line(50, y, 100, y)
        
        y -= 20
        
        # Group skills by proficiency
        skills_by_prof = {}
        for skill in resume.skills.all():
            prof = skill.proficiency
            if prof not in skills_by_prof:
                skills_by_prof[prof] = []
            skills_by_prof[prof].append(skill.name)
        
        # Display skills grouped by proficiency
        p.setFont("Helvetica", 10)
        p.setFillColor(text_color)
        
        for proficiency in ['Expert', 'Advanced', 'Intermediate', 'Beginner']:
            if proficiency in skills_by_prof:
                p.setFont("Helvetica-Bold", 10)
                p.setFillColor(primary_color)
                p.drawString(50, y, f"{proficiency}:")
                
                p.setFont("Helvetica", 10)
                p.setFillColor(text_color)
                skills_text = ', '.join(skills_by_prof[proficiency])
                
                # Word wrap skills
                max_width = width - 170
                if p.stringWidth(skills_text, "Helvetica", 10) > max_width:
                    words = skills_text.split(', ')
                    current_line = []
                    x_offset = 130
                    
                    for word in words:
                        current_line.append(word)
                        test_line = ', '.join(current_line)
                        if p.stringWidth(test_line, "Helvetica", 10) > max_width:
                            current_line.pop()
                            p.drawString(x_offset, y, ', '.join(current_line) + ',')
                            y -= 12
                            current_line = [word]
                    if current_line:
                        p.drawString(x_offset, y, ', '.join(current_line))
                        y -= 15
                else:
                    p.drawString(130, y, skills_text)
                    y -= 15
    
    # Save PDF
    p.showPage()
    p.save()
    
    # Get PDF from buffer
    buffer.seek(0)
    
    # Create HTTP response
    response = HttpResponse(buffer, content_type='application/pdf')
    filename = f"{resume.full_name.replace(' ', '_')}_Resume.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    resume.delete()
    messages.success(request, 'Resume deleted successfully!')
    return redirect('dashboard')