from django.db import models
from django.conf import settings
import uuid

class Company(models.Model):
    CATEGORY_CHOICES = [
        ('commercial',     'Commercial'),
        ('renovation',     'Renovation'),
        ('infrastructure', 'Infrastructure'),
        ('residential',    'Residential'),
        ('interior',       'Interior'),
    ]
    PLAN_CHOICES = [
        ('free',       'Basic / Free'),
        ('pro',        'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    STATUS_CHOICES = [
        ('pending',  'Pending Authority Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name='company')
    name         = models.CharField(max_length=200)
    category     = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description  = models.TextField(blank=True)
    location     = models.CharField(max_length=200)
    founded_year = models.PositiveIntegerField()
    license_no   = models.CharField(max_length=100, unique=True)
    plan         = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified     = models.BooleanField(default=False)
    rating       = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    specialties  = models.JSONField(default=list)
    logo         = models.ImageField(upload_to='companies/logos/', null=True, blank=True)
    cover_color  = models.CharField(max_length=20, default='#1a2a3a')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('license',     'Trade License'),
        ('certificate', 'Certificate'),
        ('declaration', 'Signed Declaration'),
        ('other',       'Other'),
    ]
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents')
    doc_type    = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES)
    file        = models.FileField(upload_to='companies/documents/')
    name        = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} — {self.name}"


class CompanyReview(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company    = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating     = models.PositiveSmallIntegerField()
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'author')

    def __str__(self):
        return f"{self.company.name} — {self.rating}★"