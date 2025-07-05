from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    phone_number = models.CharField(max_length=15, default="0000000000")  

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permissions',  
        blank=True
    )

from django.conf import settings
from django.db import models

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='No description')
    category = models.CharField(max_length=100, default='General')
    deadline = models.DateField(null=True, blank=True)
    pinned = models.BooleanField(default=False)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    lead = models.ForeignKey(User, related_name='led_projects', on_delete=models.SET_NULL, null=True, blank=True)
    team_members = models.ManyToManyField(User, related_name='project_team', blank=True)
    created_at = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.name



# 🔹 Task Model 
class Task(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.SET_NULL, 
    null=True, 
    blank=True,
    related_name="assigned_tasks" 
)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"