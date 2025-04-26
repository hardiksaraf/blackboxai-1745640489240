from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:venue_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:venue_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('address/', views.address_selection, name='address_selection'),
    path('order-summary/', views.order_summary, name='order_summary'),
    path('apply-promo/', views.apply_promo_code, name='apply_promo'),
]
