# 📄 Resume Builder - Professional Resume Generator

![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

A modern, full-stack web application built with Django that enables users to create, manage, and download professional resumes as PDF files. Features a sleek dark-themed UI with multi-user authentication and secure data management.

!

## 🌟 Features

### Core Functionality
- ✅ **Multi-User Authentication** - Secure registration, login, and session management
- ✅ **Resume Management** - Create, read, update, and delete multiple resumes
- ✅ **Dynamic Sections** - Add unlimited education, work experience, and skills entries
- ✅ **Professional PDF Export** - Generate ATS-friendly resumes with custom formatting
- ✅ **Responsive Design** - Mobile-first dark-themed UI with cyan/violet accents
- ✅ **Data Persistence** - PostgreSQL database with Django ORM

### Technical Features
- 🔐 Session-based authentication with CSRF protection
- 🗄️ Normalized database schema with foreign key relationships
- 📱 Responsive CSS Grid/Flexbox layout (no frameworks)
- 📄 ReportLab PDF generation with professional formatting
- 🎨 Dark theme with CSS variables and modern design
- 🚀 Production-ready deployment configuration

## 🖼️ Screenshots

### Home Page
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/a09b4560-03a5-4c20-aba9-596e2b9a72d4" />


### Dashboard
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/d3c6488a-d4d8-449c-8ce0-f339dcf74444" />


### Create Resume
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/df152d5e-7259-451c-b618-484085eccdb2" />


### Edit Resume
<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/cb17a531-d386-4487-bf5d-99816a78fd1c" />

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/2148c4c5-5278-4960-91d1-51d31d1ee494" />

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/1eb8d08d-3471-42b6-b731-ef8701e51886" />


### Generated PDF

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/fe98ce5b-498f-4981-ab33-0189f1c0d6d6" />



## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.0.1
- **Language**: Python 3.8+
- **Database**: PostgreSQL (Production), SQLite (Development)
- **PDF Generation**: ReportLab 4.0.9
- **Server**: Gunicorn (Production)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with Grid/Flexbox
- **JavaScript** - Minimal client-side interactions
- **Font Awesome** - Icons
- **Google Fonts** - Inter font family

### Deployment
- **Platform**: Render
- **Static Files**: WhiteNoise
- **Environment Management**: python-decouple

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git
- PostgreSQL (for production) - optional for local development

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/resume-builder.git
cd resume-builder
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure
```
resume_builder/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .env                      # Environment variables (not in repo)
├── .gitignore               # Git ignore rules
│
├── resume_builder/          # Main project directory
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── resumes/                 # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── resumes/
│   │       ├── base.html           # Base template
│   │       ├── home.html           # Landing page
│   │       ├── signup.html         # Registration
│   │       ├── login.html          # Login page
│   │       ├── dashboard.html      # User dashboard
│   │       ├── create_resume.html  # Create form
│   │       └── edit_resume.html    # Edit interface
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── forms.py             # Django forms
│   ├── views.py             # View functions
│   └── urls.py              # App URL patterns
│
├── media/                   # User uploaded files
├── static/                  # Static files (CSS, JS, images)
└── db.sqlite3              # SQLite database (development)
```

## 🗄️ Database Schema
```
┌─────────────────┐
│      User       │ (Django built-in)
│  - id           │
│  - username     │
│  - email        │
│  - password     │
└────────┬────────┘
         │ 1:Many
         │
┌────────▼────────┐
│     Resume      │
│  - id           │
│  - user_id (FK) │
│  - full_name    │
│  - email        │
│  - phone        │
│  - address      │
│  - summary      │
│  - created_at   │
│  - updated_at   │
└────────┬────────┘
         │
    ┌────┼────┬────────┐
    │    │    │        │
┌───▼──┐ │ ┌──▼───┐ ┌─▼──────┐
│ Edu  │ │ │ Exp  │ │ Skill  │
│      │ │ │      │ │        │
└──────┘ │ └──────┘ └────────┘
         │
      (1:Many relationships)
```

## 🔑 Key Features Explained

### 1. Authentication System
- **Registration**: Users create accounts with username, email, and password
- **Login**: Session-based authentication using Django's built-in system
- **Password Security**: PBKDF2 hashing with salt
- **Session Management**: Secure cookies and CSRF protection

### 2. Resume Management
- **CRUD Operations**: Full create, read, update, delete functionality
- **Multiple Resumes**: Users can create unlimited resumes
- **Data Validation**: Form validation before database storage
- **Timestamps**: Automatic created_at and updated_at tracking

### 3. PDF Generation
- **ReportLab Integration**: Python library for PDF creation
- **Professional Formatting**: 
  - Custom fonts and colors
  - Section headers with accent lines
  - Bullet points for descriptions
  - Right-aligned dates
  - Footer with generation timestamp
- **ATS-Friendly**: Clean structure for Applicant Tracking Systems

### 4. UI/UX Design
- **Dark Theme**: Background gradient (#0f0f10 → #1a1a1d)
- **Accent Colors**: Cyan (#00d9ff) and Violet (#8b5cf6)
- **Fixed Navigation**: Stays at top while scrolling
- **Responsive**: CSS Grid and Flexbox for all screen sizes
- **No Framework**: Vanilla CSS to demonstrate fundamentals

## 🎨 Color Palette
```css
--bg-dark: #0f0f10;        /* Main background */
--bg-card: #1e1e22;        /* Cards and sections */
--text-primary: #e8e8ee;   /* Main text */
--text-secondary: #a8a8b8; /* Secondary text */
--accent-cyan: #00d9ff;    /* Primary accent */
--accent-violet: #8b5cf6;  /* Secondary accent */
--success: #10b981;        /* Success messages */
--danger: #ef4444;         /* Error messages */
```

## 🚢 Deployment to Render
https://resume-builder-u93s.onrender.com/


## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔮 Future Enhancements

- [ ] Multiple resume templates (Modern, Classic, Creative)
- [ ] Profile photo upload for resumes
- [ ] Email verification for new accounts
- [ ] Export to DOCX format
- [ ] Resume preview before download
- [ ] Public resume sharing with unique URLs
- [ ] Resume analytics (views, downloads)
- [ ] AI-powered resume suggestions
- [ ] Cover letter generator
- [ ] Integration with LinkedIn


## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [ReportLab Documentation](https://www.reportlab.com/docs/)
- [Font Awesome](https://fontawesome.com/) for icons
- [Google Fonts](https://fonts.google.com/) for Inter font
- [Render](https://render.com/) for hosting

⭐ If you find this project useful, please give it a star on GitHub!
