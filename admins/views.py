from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from .models import AdminAnalytics, UserReport

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and user.is_admin_user

@user_passes_test(is_admin)
def dashboard(request):
    analytics = AdminAnalytics.objects.order_by('-date').first()
    reports = UserReport.objects.filter(resolved=False).order_by('-created_at')
    context = {
        'analytics': analytics,
        'reports': reports,
    }
    return render(request, 'admins/dashboard.html', context)

@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    context = {'users': users}
    return render(request, 'admins/manage_users.html', context)

@user_passes_test(is_admin)
def manage_vendors(request):
    vendors = User.objects.filter(is_vendor=True).order_by('-date_joined')
    context = {'vendors': vendors}
    return render(request, 'admins/manage_vendors.html', context)

@user_passes_test(is_admin)
def reports(request):
    reports = UserReport.objects.all().order_by('-created_at')
    context = {'reports': reports}
    return render(request, 'admins/reports.html', context)

@user_passes_test(is_admin)
def resolve_report(request, report_id):
    report = get_object_or_404(UserReport, id=report_id)
    if request.method == 'POST':
        report.resolved = True
        report.resolved_by = request.user
        report.save()
        return redirect('admins:reports')
    context = {'report': report}
    return render(request, 'admins/resolve_report.html', context)
