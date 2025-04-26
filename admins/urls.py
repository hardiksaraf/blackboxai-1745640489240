from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('vendors/', views.manage_vendors, name='manage_vendors'),
    path('reports/', views.reports, name='reports'),
    path('reports/resolve/<int:report_id>/', views.resolve_report, name='resolve_report'),
]
