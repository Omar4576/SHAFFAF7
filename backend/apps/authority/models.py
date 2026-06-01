from django.db import models
from django.conf import settings
import uuid

class AuthorityReview(models.Model):
    DECISION_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('changes',  'Changes Requested'),
        ('rejected', 'Rejected'),
    ]
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project     = models.OneToOneField('projects.Project', on_delete=models.CASCADE,
                                        related_name='authority_review')
    reviewer    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='reviews_given')
    decision    = models.CharField(max_length=20, choices=DECISION_CHOICES, default='pending')
    notes       = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} — {self.decision}"


class AuthorityNote(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review     = models.ForeignKey(AuthorityReview, on_delete=models.CASCADE,
                                    related_name='note_list')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True)
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']