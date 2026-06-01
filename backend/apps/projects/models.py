from django.db import models
from django.conf import settings
import uuid

class Project(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('pending',   'Pending Authority Approval'),
        ('approved',  'Approved / Live'),
        ('rejected',  'Rejected'),
        ('completed', 'Completed'),
    ]

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company          = models.ForeignKey('companies.Company', on_delete=models.CASCADE,
                                          related_name='projects')
    name             = models.CharField(max_length=300)
    description      = models.TextField(blank=True)
    location         = models.CharField(max_length=300)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress_pct     = models.PositiveSmallIntegerField(default=0)
    total_floors     = models.PositiveIntegerField(default=1)
    completed_floors = models.PositiveIntegerField(default=0)
    total_units      = models.PositiveIntegerField(default=0)
    handover_date    = models.DateField(null=True, blank=True)
    cover_color      = models.CharField(max_length=20, default='#1a2a3a')
    supplier         = models.CharField(max_length=300, blank=True)
    materials_info   = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class ProjectMilestone(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name        = models.CharField(max_length=300)
    done        = models.BooleanField(default=False)
    target_date = models.DateField(null=True, blank=True)
    pct         = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['target_date']


class ProjectUpdate(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project    = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    class Meta:
        ordering = ['-created_at']


class VideoUpdate(models.Model):
    VIDEO_TYPE = [
        ('structure', 'Structure'),
        ('authority', 'Authority Inspection'),
        ('unit',      'Unit View'),
        ('amenity',   'Amenity'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Upload'),
        ('ready',   'Ready'),
        ('rec',     'Live / Recording'),
    ]
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos')
    title       = models.CharField(max_length=300)
    area        = models.CharField(max_length=300, blank=True)
    video_type  = models.CharField(max_length=20, choices=VIDEO_TYPE, default='structure')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    duration    = models.CharField(max_length=10, blank=True)
    file        = models.FileField(upload_to='projects/videos/', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class UnitRecord(models.Model):
    HANDOVER_STATUS = [
        ('structure_complete', 'Structure Complete'),
        ('mep_in_progress',    'MEP In Progress'),
        ('finishing',          'Finishing'),
        ('ready',              'Ready for Handover'),
        ('handed_over',        'Handed Over'),
    ]
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='units')
    floor       = models.PositiveIntegerField()
    unit        = models.CharField(max_length=20)
    unit_type   = models.CharField(max_length=100, blank=True)
    status      = models.CharField(max_length=30, choices=HANDOVER_STATUS,
                                    default='structure_complete')
    ready       = models.BooleanField(default=False)
    buyer       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='units')
    latest_video= models.CharField(max_length=300, blank=True)
    notes       = models.TextField(blank=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'floor', 'unit')
        ordering = ['floor', 'unit']

    def __str__(self):
        return f"{self.project.name} — Floor {self.floor} Unit {self.unit}"