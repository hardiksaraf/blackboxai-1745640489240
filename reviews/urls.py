from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('submit/<int:venue_id>/', views.submit_review, name='submit_review'),
    path('view/<int:venue_id>/', views.view_reviews, name='view_reviews'),
    path('comment/<int:review_id>/', views.add_comment, name='add_comment'),
]
