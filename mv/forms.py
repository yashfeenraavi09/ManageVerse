from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser 
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

from .models import Project

from django import forms
from .models import Project
from django import forms
from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

from django import forms
from .models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'category', 'deadline', 'team_members', 'lead']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'lead': forms.Select(attrs={'class': 'form-control'}),
            'team_members': forms.SelectMultiple(attrs={'class': 'form-control'}),  
            'category': forms.TextInput(attrs={'placeholder': 'e.g., Web, ML, Design'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['lead'].queryset = User.objects.all()
        self.fields['team_members'].queryset = User.objects.all() 

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "status", "deadline"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "assigned_to": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

from django import forms
from .models import Project

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["deadline"]
        widgets = {
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write your comment...'})
        }
