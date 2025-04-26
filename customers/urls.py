from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/add/', views.add_address, name='add_address'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('saved-cards/', views.saved_cards_view, name='saved_cards'),
]
