from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    
    # Profile Management
    path('profile/', views.profile, name='profile'),
    path('change-email/', views.change_email, name='change_email'),
    path('verify-email-change/<str:token>/', views.verify_email_change, name='verify_email_change'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
