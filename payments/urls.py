from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('gateway/<int:booking_id>/', views.payment_gateway, name='payment_gateway'),
    path('receipt/<int:booking_id>/', views.payment_receipt, name='receipt'),
    path('refund/<int:transaction_id>/', views.refund_request, name='refund_request'),
    path('saved-cards/', views.saved_cards, name='saved_cards'),
]
