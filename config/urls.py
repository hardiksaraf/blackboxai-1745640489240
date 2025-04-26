from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('customers/', include('customers.urls')),
    path('vendors/', include('vendors.urls')),
    path('admins/', include('admins.urls')),
    path('listings/', include('listings.urls')),
    path('bookings/', include('bookings.urls')),
    path('checkout/', include('checkout.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('support/', include('support.urls')),
    path('notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
