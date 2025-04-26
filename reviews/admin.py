from django.contrib import admin
from .models import Review, ReviewComment

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'venue', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('customer__email', 'venue__title', 'comment')
    ordering = ('-created_at',)

@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'commenter', 'timestamp')
    search_fields = ('commenter__email', 'comment_text')
    ordering = ('-timestamp',)
