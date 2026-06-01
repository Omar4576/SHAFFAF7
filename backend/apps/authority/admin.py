from django.contrib import admin
from .models import AuthorityReview, AuthorityNote

@admin.register(AuthorityReview)
class AuthorityReviewAdmin(admin.ModelAdmin):
    list_display  = ['project', 'decision', 'reviewer', 'reviewed_at']
    list_filter   = ['decision']

admin.site.register(AuthorityNote)