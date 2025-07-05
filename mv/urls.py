from django.contrib import admin
from django.urls import path
from mv import views
from .views import dashboard, pin_project, unpin_project
from .views import pin_project, unpin_project, assign_task,view_deadline, set_deadline
from .views import add_project 

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("features", views.features, name='features'),
    path("contact", views.contact, name='contact'),
    path('submit-contact-form', views.submit_contact_form, name='submit_contact_form'),
    path("login", views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'), 
    path("choose-role/", views.role_selection, name="choose_role"),
    path("signup/manager/", views.signup_manager, name="signup_manager"),
    path("signup/user/", views.signup_user, name="signup_user"),
    path("privacy_policy", views.privacy_policy, name='privacy_policy'),
    path("terms_of_service", views.terms_of_service, name='terms_of_service'),
    path('dashboard', views.dashboard, name='dashboard'),
     path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('manager_dashboard', views.manager_dashboard, name='manager_dashboard'),
    path("add_project/", add_project, name="add_project"),
    path('pin_project/<int:project_id>/', pin_project, name='pin_project'),
    path('unpin_project/<int:project_id>/', unpin_project, name='unpin_project'),
    path('assign_task/<int:project_id>/', assign_task, name='assign_task'),
    path('project/<int:project_id>/set_deadline/', set_deadline, name='set_deadline'),
    path("view-deadline/<int:project_id>/", view_deadline, name="view_deadline"),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('assign_task/<int:project_id>/', assign_task, name='assign_task'),
    path('settings/', views.settings_page, name='settings_page'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout_all/', views.logout_all, name='logout_all'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('projects/' , views.manager_projects , name='projects_page') ,
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('tasks/<int:task_id>/complete/', views.mark_task_completed, name='mark_task_completed'),
]
