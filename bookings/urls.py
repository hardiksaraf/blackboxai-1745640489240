from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:venue_id>/', views.create_booking, name='create'),
    path('detail/<int:booking_id>/', views.booking_detail, name='detail'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel'),
    path('reschedule/<int:booking_id>/', views.reschedule_booking, name='reschedule'),
]
