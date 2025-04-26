from django.conf import settings
from .models import SiteConfiguration

def site_settings(request):
    """
    Add site configuration to the template context
    """
    try:
        config = SiteConfiguration.objects.first()
    except:
        config = None

    return {
        'site_config': config,
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'RentMyVenue'),
        'CONTACT_EMAIL': getattr(settings, 'CONTACT_EMAIL', 'info@rentmyvenue.com'),
        'CONTACT_PHONE': getattr(settings, 'CONTACT_PHONE', '1-800-VENUE'),
        'SOCIAL_LINKS': {
            'facebook': getattr(settings, 'FACEBOOK_URL', '#'),
            'twitter': getattr(settings, 'TWITTER_URL', '#'),
            'instagram': getattr(settings, 'INSTAGRAM_URL', '#'),
            'linkedin': getattr(settings, 'LINKEDIN_URL', '#'),
        },
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
    }

def user_notifications(request):
    """
    Add user notifications to the template context
    """
    if not request.user.is_authenticated:
        return {'notifications': []}

    # Get user's unread notifications
    notifications = request.user.notifications.filter(
        read=False
    ).order_by('-created_at')[:5]

    return {
        'notifications': notifications,
        'unread_count': notifications.count(),
    }

def active_venues(request):
    """
    Add active venues count and featured venues to the template context
    """
    try:
        from listings.models import Venue
        active_venues_count = Venue.objects.filter(is_active=True).count()
        featured_venues = Venue.objects.filter(
            is_active=True,
            is_featured=True
        ).order_by('-created_at')[:3]
    except:
        active_venues_count = 0
        featured_venues = []

    return {
        'active_venues_count': active_venues_count,
        'featured_venues': featured_venues,
    }

def search_form(request):
    """
    Add search form to the template context
    """
    try:
        from core.forms import SearchForm
        search_form = SearchForm(request.GET or None)
    except:
        search_form = None

    return {
        'search_form': search_form,
    }

def footer_content(request):
    """
    Add footer content to the template context
    """
    try:
        from core.models import FAQ
        faqs = FAQ.objects.filter(
            is_published=True
        ).order_by('category', 'order')[:5]
    except:
        faqs = []

    return {
        'footer_faqs': faqs,
        'current_year': settings.CURRENT_YEAR if hasattr(settings, 'CURRENT_YEAR') else None,
    }

def meta_defaults(request):
    """
    Add default meta tags to the template context
    """
    return {
        'default_meta_title': 'RentMyVenue - Find and Book Perfect Venues',
        'default_meta_description': 'Discover and book unique venues for your events. '
                                  'From intimate gatherings to large celebrations, find the perfect space.',
        'default_meta_keywords': 'venue rental, event space, booking platform, event venues',
        'default_meta_image': f'{settings.STATIC_URL}img/og-image.jpg',
    }
