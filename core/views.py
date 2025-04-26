from django.shortcuts import render
from django.db.models import Count, Avg
from listings.models import Venue, VenueType
from reviews.models import Review

def home(request):
    """Home page view"""
    # Get featured venues (top rated with at least 3 reviews)
    featured_venues = Venue.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).filter(
        review_count__gte=3,
        is_active=True
    ).order_by('-avg_rating')[:6]
    
    # Get popular venue types
    popular_types = VenueType.objects.annotate(
        venue_count=Count('venues')
    ).filter(
        venue_count__gt=0
    ).order_by('-venue_count')[:6]
    
    # Get latest reviews
    latest_reviews = Review.objects.select_related(
        'venue', 'customer'
    ).filter(
        is_approved=True
    ).order_by('-created_at')[:3]
    
    context = {
        'featured_venues': featured_venues,
        'popular_types': popular_types,
        'latest_reviews': latest_reviews,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    # Get some statistics for the about page
    stats = {
        'total_venues': Venue.objects.filter(is_active=True).count(),
        'total_bookings': 1000,  # You would get this from your bookings model
        'happy_customers': 500,   # This could be users with successful bookings
        'cities_covered': 50,     # This could be unique cities from your venues
    }
    
    context = {
        'stats': stats,
        'team_members': [
            {
                'name': 'John Doe',
                'position': 'CEO & Founder',
                'image': 'team/john-doe.jpg',
                'bio': 'Passionate about connecting people with perfect venues.'
            },
            {
                'name': 'Jane Smith',
                'position': 'Head of Operations',
                'image': 'team/jane-smith.jpg',
                'bio': 'Expert in customer service and venue management.'
            },
            # Add more team members as needed
        ]
    }
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page view"""
    return render(request, 'core/contact.html')

def terms(request):
    """Terms of service page view"""
    return render(request, 'core/terms.html')

def privacy(request):
    """Privacy policy page view"""
    return render(request, 'core/privacy.html')

def faq(request):
    """FAQ page view"""
    faqs = [
        {
            'category': 'General',
            'questions': [
                {
                    'question': 'How does RentMyVenue work?',
                    'answer': 'RentMyVenue connects venue owners with people looking to rent spaces for events. Browse venues, check availability, and book directly through our platform.'
                },
                {
                    'question': 'Is it free to use RentMyVenue?',
                    'answer': 'It's free to browse venues and create an account. We charge a small service fee only when you make a booking.'
                },
            ]
        },
        {
            'category': 'Bookings',
            'questions': [
                {
                    'question': 'How do I make a booking?',
                    'answer': 'Select your desired venue, check availability for your dates, and follow the booking process. You can pay securely through our platform.'
                },
                {
                    'question': 'What is your cancellation policy?',
                    'answer': 'Cancellation policies vary by venue. Each venue listing clearly displays their specific cancellation terms.'
                },
            ]
        },
        {
            'category': 'Payments',
            'questions': [
                {
                    'question': 'What payment methods do you accept?',
                    'answer': 'We accept all major credit cards, debit cards, and digital wallets through our secure payment system.'
                },
                {
                    'question': 'Is my payment secure?',
                    'answer': 'Yes, all payments are processed through our secure payment gateway with industry-standard encryption.'
                },
            ]
        },
    ]
    return render(request, 'core/faq.html', {'faqs': faqs})

def error_404(request, exception):
    """404 error page view"""
    return render(request, 'core/404.html', status=404)

def error_500(request):
    """500 error page view"""
    return render(request, 'core/500.html', status=500)
