from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project

@receiver(post_save, sender=Project)
def create_authority_review(sender, instance, created, **kwargs):
    if created:
        from apps.authority.models import AuthorityReview
        AuthorityReview.objects.get_or_create(project=instance)