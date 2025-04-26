from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, ReviewComment
from listings.models import Venue

@login_required
def submit_review(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()
        if rating < 1 or rating > 5:
            messages.error(request, "Invalid rating value.")
            return redirect('listings:detail', venue_id=venue.id)
        if not comment:
            messages.error(request, "Comment cannot be empty.")
            return redirect('listings:detail', venue_id=venue.id)
        review = Review.objects.create(
            customer=request.user,
            venue=venue,
            rating=rating,
            comment=comment,
            is_approved=False  # Needs moderation
        )
        messages.success(request, "Review submitted successfully and is pending approval.")
        return redirect('listings:detail', venue_id=venue.id)
    return render(request, 'reviews/submit_review.html', {'venue': venue})

@login_required
def view_reviews(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    reviews = Review.objects.filter(venue=venue, is_approved=True).order_by('-created_at')
    return render(request, 'reviews/view_reviews.html', {'venue': venue, 'reviews': reviews})

@login_required
def add_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text', '').strip()
        if not comment_text:
            messages.error(request, "Comment cannot be empty.")
            return redirect('reviews:view_reviews', venue_id=review.venue.id)
        ReviewComment.objects.create(
            review=review,
            commenter=request.user,
            comment_text=comment_text
        )
        messages.success(request, "Comment added successfully.")
        return redirect('reviews:view_reviews', venue_id=review.venue.id)
    return render(request, 'reviews/add_comment.html', {'review': review})
