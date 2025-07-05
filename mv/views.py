from django.shortcuts import render , HttpResponse , redirect
from datetime import datetime
from mv.models import Contact
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .forms import SignupForm
from django.db import models  
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(request):
    return render(request , 'home.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')
from django.shortcuts import render

def contact(request):
    return render(request, 'contact.html')

from .models import Contact 

def submit_contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            messages.success(request, 'Thank you for contacting us. We appreciate your inquiry and will get back to you shortly.')
            return redirect('contact')  

    return render(request, 'contact.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!", extra_tags="auth_success")

            if user.role == 'manager':
                return redirect('manager_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    return render(request, 'login.html')


from django.shortcuts import redirect

from django.shortcuts import render, redirect

def role_selection(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role == 'manager':
            return redirect('signup_manager')
        elif role == 'user':
            return redirect('signup_user')
    return render(request, 'choose_role.html')



from .forms import SignupForm 

def signup_manager(request):
    """Signup view for Manager role"""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "manager"
            user.save()
            messages.success(request, "Manager account created successfully!")
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup_manager.html", {"form": form})

def signup_user(request):
    """Signup view for User role"""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "user" 
            user.save()
            messages.success(request, "User account created successfully!")
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup_user.html", {"form": form})


from .models import Project
from .forms import ProjectForm
from .models import Project, Task


@login_required
def dashboard(request):
    user = request.user

    # Get all projects for the logged-in user
    projects = Project.objects.filter(user=user)

    # Get all pinned projects
    pinned_projects = projects.filter(pinned=True)

    # Get all tasks related to user's projects
    tasks = Task.objects.filter(project__in=projects)

    # Get completed tasks for progress tracking
    completed_tasks = tasks.filter(status="Completed").count()
    total_tasks = tasks.count()
    progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Get upcoming deadlines (projects with deadlines approaching)
    upcoming_deadlines = projects.filter(deadline__isnull=False).order_by("deadline")


    # Daily Goals Example (Customize as needed)
    daily_goal = "Complete at least 2 tasks"
    streak_days = 5  # Example streak value

    context = {
        "projects": projects,
        "pinned_projects": pinned_projects,
        "tasks": tasks,
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "progress_percentage": progress_percentage,
        "upcoming_deadlines": upcoming_deadlines,
        "daily_goal": daily_goal,
        "streak_days": streak_days,
    }

    return render(request, "dashboard.html", context)

from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Project
from .forms import ProjectForm

User = get_user_model()

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user 
            lead_id = request.POST.get('lead')
            if lead_id:
                project.lead = User.objects.get(id=lead_id)
            project.category = request.POST.get('category')
            project.save()

            # Assign team members
            team_member_ids = request.POST.getlist('team_members')
            team_members = User.objects.filter(id__in=team_member_ids)
            project.team_members.set(team_members)

            return redirect('manager_dashboard')
    else:
        form = ProjectForm()

    users = User.objects.all()
    return render(request, 'manager_dashboard.html', {'form': form, 'users': users})


# Logout View 
from django.contrib.auth import logout
def custom_logout(request):
    logout(request)
    return redirect('login') 

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Project


def pin_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.user == request.user or request.user in project.team_members.all():
        project.pinned = True
        project.save()
        messages.success(request, f"'{project.name}' has been pinned!")
    else:
        messages.error(request, "You are not authorized to pin this project.")

    return redirect_back_to_dashboard(request)


def unpin_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.user == request.user or request.user in project.team_members.all():
        project.pinned = False
        project.save()
        messages.success(request, f"'{project.name}' has been unpinned!")
    else:
        messages.error(request, "You are not authorized to unpin this project.")

    return redirect_back_to_dashboard(request)

def redirect_back_to_dashboard(request):
    if request.user.role == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('manager_dashboard')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

from .models import Project, Task

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, Task
from .forms import TaskForm 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, Task
from .forms import TaskForm

@login_required
def assign_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    # Filter only team members of the project for assignment
    team_members = project.team_members.all()

    if request.method == "POST":
        form = TaskForm(request.POST)
        form.fields["assigned_to"].queryset = team_members  # Set team member options

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, f"Task '{task.title}' assigned successfully!")
            return redirect('manager_dashboard')
    else:
        form = TaskForm()
        form.fields["assigned_to"].queryset = team_members  

    return render(request, 'assign_task.html', {'form': form, 'project': project})

def view_deadline(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    return render(request, 'view_deadline.html', {'project': project})

from .forms import DeadlineForm

def set_deadline(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = DeadlineForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Deadline set successfully!")
            return redirect('manager_dashboard')
    else:
        form = DeadlineForm(instance=project)

    return render(request, 'set_deadline.html', {'form': form, 'project': project})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import logout

@login_required
def settings_page(request):
    return render(request, 'settings.html')

@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Profile updated successfully!")
    return redirect('settings_page')

@login_required
def change_password(request):
    if request.method == "POST":
        user = request.user
        new_password = request.POST.get("new_password")
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Keep user logged in
        messages.success(request, "Password changed successfully!")
    return redirect('settings_page')

@login_required
def logout_all(request):
    logout(request)
    messages.success(request, "Logged out from all devices!")
    return redirect('login')

@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect('home')

def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # Deletes the user account
        logout(request)  # Logs out the user
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Redirect to homepage or login page
    
    return redirect('settings_page')  # If accessed via GET, go back to settings

@login_required
def manager_projects(request):
    projects = Project.objects.filter(user=request.user) | Project.objects.filter(team_members=request.user)
    projects = projects.distinct()

    total_tasks = sum(project.tasks.count() for project in projects)
    completed_tasks = sum(project.tasks.filter(status='completed').count() for project in projects)
    pending_tasks = total_tasks - completed_tasks

    progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0

    project_chart = generate_project_bar_chart(projects)

    return render(request, 'projects.html', {
        'projects': projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress_percentage': progress_percentage,
        'project_chart': project_chart
    })


@login_required
def user_dashboard(request):
    projects = Project.objects.filter(team_members=request.user)
    return render(request, 'manager_dashboard.html', {'projects': projects})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Project, Task
from .forms import ProjectForm

import matplotlib.pyplot as plt
import io
import base64

User = get_user_model()

@login_required
def manager_dashboard(request):
    user = request.user

    if user.role == 'manager':
        projects = Project.objects.filter(user=user)
    else:
        projects = Project.objects.filter(team_members=user)

    pinned_projects = projects.filter(pinned=True)

    tasks = Task.objects.filter(project__in=projects)
    completed_tasks = tasks.filter(status="Completed").count()
    total_tasks = tasks.count()
    pending_tasks = total_tasks - completed_tasks
    progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    project_chart = None
  

    upcoming_deadlines = projects.filter(deadline__isnull=False).order_by("deadline")

    daily_goal = "Complete at least 2 tasks"
    streak_days = 5  

    form = ProjectForm()
    users = User.objects.all()

    context = {
        'form': form,
        'users': users,
        'projects': projects,
        'pinned_projects': pinned_projects,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'progress_percentage': progress_percentage,
        'upcoming_deadlines': upcoming_deadlines,
        'daily_goal': daily_goal,
        'streak_days': streak_days,
        'project_chart': project_chart, 
    }

    return render(request, 'manager_dashboard.html', context)



import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project
import matplotlib
matplotlib.use('Agg') 

def generate_project_bar_chart(projects):
    labels = []
    completion_rates = []

    for project in projects:
        total_tasks = project.tasks.count()
        completed_tasks = project.tasks.filter(status='Completed').count() 

        if total_tasks > 0:
            percent = (completed_tasks / total_tasks) * 100
        else:
            percent = 0

        labels.append(project.name)
        completion_rates.append(percent)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(labels, completion_rates, color='#4CAF50')
    ax.set_xlabel('Completion %')
    ax.set_title('Task Completion Per Project')
    ax.set_xlim(0, 100)

  
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2,
                f'{width:.1f}%', va='center')

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return image_base64


from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, Comment
from .forms import CommentForm

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all().order_by('-timestamp')
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.task = task
            new_comment.user = request.user
            new_comment.save()
            return redirect('task_detail', task_id=task.id)

    return render(request, 'task_detail.html', {
        'task': task,
        'comments': comments,
        'form': form
    })


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect('manager_dashboard')

    messages.error(request, "Invalid request method.")
    return redirect('manager_dashboard')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Task

@login_required
def mark_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if task.status != 'Completed':
        task.status = 'Completed'
        task.save()

    # Redirect based on role
    if request.user.role == 'manager':
        return redirect('manager_dashboard')
    else:
        return redirect('manager_dashboard')  
