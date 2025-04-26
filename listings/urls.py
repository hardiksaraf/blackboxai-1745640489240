from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.list_venues, name='list'),
    path('search/', views.search_venues, name='search'),
    path('<int:venue_id>/', views.venue_detail, name='detail'),
]
