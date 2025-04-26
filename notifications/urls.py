from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
    path('toggle-read/<int:notification_id>/', views.toggle_notification_read, name='toggle_notification_read'),
    path('preferences/', views.preferences, name='preferences'),
]
