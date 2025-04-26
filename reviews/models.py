from django.db import models
from django.contrib.auth import get_user_model
from listings.models import Venue

User = get_user_model()

class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.customer.email} for {self.venue.title}"

class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_comments')
    comment_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review Comment"
        verbose_name_plural = "Review Comments"

    def __str__(self):
        return f"Comment by {self.commenter.email} on review {self.review.id}"
