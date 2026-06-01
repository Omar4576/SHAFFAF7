from django.db import models
from django.conf import settings
import uuid

class SignedDocument(models.Model):
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name='signed_documents')
    project        = models.ForeignKey('projects.Project', on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='signed_documents')
    file_name      = models.CharField(max_length=300)
    file           = models.FileField(upload_to='documents/signed/')
    signer_name    = models.CharField(max_length=200)
    signed_at      = models.DateTimeField(auto_now_add=True)
    audit_id       = models.CharField(max_length=100, unique=True, editable=False)
    signature_page = models.PositiveSmallIntegerField(default=1)
    signature_x    = models.FloatField(default=0.72)
    signature_y    = models.FloatField(default=0.78)

    def save(self, *args, **kwargs):
        if not self.audit_id:
            import secrets
            self.audit_id = f"SHA-{secrets.token_hex(8).upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_name} — {self.audit_id}"