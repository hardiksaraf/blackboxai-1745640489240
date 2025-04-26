from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Venue, VenueType, Feature, Gallery, AvailabilityCalendar

def list_venues(request):
    venues = Venue.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(venues, 10)  # 10 venues per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'listings/list.html', context)

def venue_detail(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id, is_active=True)
    features = Feature.objects.filter(venue=venue)
    gallery = Gallery.objects.filter(venue=venue)
    availability = AvailabilityCalendar.objects.filter(venue=venue)
    context = {
        'venue': venue,
        'features': features,
        'gallery': gallery,
        'availability': availability,
    }
    return render(request, 'listings/detail.html', context)

def search_venues(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    venues = Venue.objects.filter(is_active=True)
    if query:
        venues = venues.filter(title__icontains=query)
    if location:
        venues = venues.filter(address__icontains=location)
    paginator = Paginator(venues, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'query': query,
        'location': location,
    }
    return render(request, 'listings/search_results.html', context)
