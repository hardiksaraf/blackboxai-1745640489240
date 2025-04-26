from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    default_address = models.ForeignKey('AddressBook', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return self.full_name

class AddressBook(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=20, choices=[('billing', 'Billing'), ('shipping', 'Shipping')])
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line1}, {self.city}"

class SavedCards(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='saved_cards')
    card_last4 = models.CharField(max_length=4)
    card_type = models.CharField(max_length=50)
    expiry_month = models.PositiveSmallIntegerField()
    expiry_year = models.PositiveSmallIntegerField()
    gateway_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.card_type} ****{self.card_last4}"

class Wishlist(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='wishlists')
    venue = models.ForeignKey('listings.Venue', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'venue')

    def __str__(self):
        return f"{self.customer.full_name} - {self.venue.title}"
