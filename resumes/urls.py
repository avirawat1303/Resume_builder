from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_resume, name='create_resume'),
    path('edit/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    path('download/<int:resume_id>/', views.download_resume, name='download_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('add-education/<int:resume_id>/', views.add_education, name='add_education'),
    path('add-experience/<int:resume_id>/', views.add_experience, name='add_experience'),
    path('add-skill/<int:resume_id>/', views.add_skill, name='add_skill'),
]