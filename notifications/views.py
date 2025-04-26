from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification, ChannelPreference

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})

@login_required
def toggle_notification_read(request, notification_id):
    notification = Notification.objects.filter(id=notification_id, user=request.user).first()
    if notification:
        notification.read = not notification.read
        notification.save()
    return redirect('notifications:notifications_list')

@login_required
def preferences(request):
    preferences, created = ChannelPreference.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        email_enabled = request.POST.get('email_enabled') == 'on'
        sms_enabled = request.POST.get('sms_enabled') == 'on'
        push_enabled = request.POST.get('push_enabled') == 'on'
        preferences.email_enabled = email_enabled
        preferences.sms_enabled = sms_enabled
        preferences.push_enabled = push_enabled
        preferences.save()
        return redirect('notifications:preferences')
    return render(request, 'notifications/preferences.html', {'preferences': preferences})
