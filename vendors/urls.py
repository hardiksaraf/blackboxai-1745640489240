from django.urls import path
from . import views

app_name = 'vendors'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('kyc/upload/', views.kyc_upload, name='kyc_upload'),
    path('listings/', views.listing_management, name='listing_management'),
]
