from django.contrib import admin
from .models import CustomerProfile, AddressBook, SavedCards, Wishlist

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'date_of_birth')
    search_fields = ('user__email', 'full_name')

@admin.register(AddressBook)
class AddressBookAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_line1', 'city', 'state', 'country', 'is_default')
    search_fields = ('customer__user__email', 'address_line1', 'city')
    list_filter = ('is_default', 'address_type')

@admin.register(SavedCards)
class SavedCardsAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_type', 'card_last4', 'expiry_month', 'expiry_year')
    search_fields = ('customer__user__email', 'card_last4')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'venue', 'added_at')
    search_fields = ('customer__user__email', 'venue__title')
