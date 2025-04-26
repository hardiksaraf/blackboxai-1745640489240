from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('submit/', views.submit_ticket, name='submit_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('categories/', views.category_list, name='category_list'),
]
