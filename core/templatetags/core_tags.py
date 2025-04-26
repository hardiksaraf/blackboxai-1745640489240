from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import date as date_filter
import json

register = template.Library()

@register.filter
def get_range(value):
    """
    Returns a range of numbers.
    Usage: {% for i in 5|get_range %}
    """
    return range(int(value))

@register.filter
def star_rating(value):
    """
    Converts a numeric rating to star icons.
    Usage: {{ venue.rating|star_rating }}
    """
    full_stars = int(value)
    half_star = value - full_stars >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)
    
    stars = '<i class="fas fa-star text-yellow-400"></i>' * full_stars
    if half_star:
        stars += '<i class="fas fa-star-half-alt text-yellow-400"></i>'
    stars += '<i class="far fa-star text-yellow-400"></i>' * empty_stars
    
    return mark_safe(stars)

@register.filter
def price_format(value):
    """
    Formats a price with currency symbol and thousands separator.
    Usage: {{ venue.price|price_format }}
    """
    try:
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return value

@register.filter
def json_script_escape(value):
    """
    Escapes a value for use in a JSON script tag.
    Usage: {{ data|json_script_escape }}
    """
    return mark_safe(json.dumps(value))

@register.simple_tag
def query_transform(request, **kwargs):
    """
    Returns the URL-encoded query string with updated parameters.
    Usage: {% query_transform request page=2 sort='price' %}
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        updated[key] = value
    return updated.urlencode()

@register.filter
def format_phone(value):
    """
    Formats a phone number consistently.
    Usage: {{ user.phone_number|format_phone }}
    """
    if not value:
        return ''
    
    # Remove all non-digits
    phone = ''.join(filter(str.isdigit, str(value)))
    
    if len(phone) == 10:
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    elif len(phone) == 11 and phone[0] == '1':
        return f"+1 ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
    return value

@register.filter
def time_since(value):
    """
    Returns a human-readable time difference.
    Usage: {{ comment.created_at|time_since }}
    """
    from django.utils.timesince import timesince
    from django.utils.timezone import now
    
    try:
        difference = now() - value
        if difference.days > 30:
            return date_filter(value, "M d, Y")
        return f"{timesince(value)} ago"
    except (ValueError, TypeError):
        return value

@register.filter
def truncate_chars(value, max_length=50):
    """
    Truncates a string to a maximum length, adding ellipsis if needed.
    Usage: {{ venue.description|truncate_chars:100 }}
    """
    if not value:
        return ''
    
    if len(value) <= max_length:
        return value
        
    truncated = value[:max_length].rsplit(' ', 1)[0]
    return f"{truncated}..."

@register.simple_tag
def get_verbose_name(instance, field_name):
    """
    Returns the verbose name of a model field.
    Usage: {% get_verbose_name venue 'capacity' %}
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.filter
def format_address(address_dict):
    """
    Formats an address dictionary into a human-readable string.
    Usage: {{ venue.address|format_address }}
    """
    if not isinstance(address_dict, dict):
        return address_dict
    
    parts = []
    if address_dict.get('street'):
        parts.append(address_dict['street'])
    if address_dict.get('city'):
        parts.append(address_dict['city'])
    if address_dict.get('state'):
        parts.append(address_dict['state'])
    if address_dict.get('postal_code'):
        parts.append(address_dict['postal_code'])
    if address_dict.get('country'):
        parts.append(address_dict['country'])
    
    return ', '.join(parts)

@register.inclusion_tag('core/tags/social_share.html')
def social_share_buttons(url, title):
    """
    Renders social sharing buttons.
    Usage: {% social_share_buttons request.build_absolute_uri venue.title %}
    """
    return {
        'url': url,
        'title': title,
    }

@register.inclusion_tag('core/tags/pagination.html')
def pagination(page_obj):
    """
    Renders a pagination component.
    Usage: {% pagination page_obj %}
    """
    return {
        'page_obj': page_obj,
    }
