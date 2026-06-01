from django.contrib import admin
from .models import Project, ProjectMilestone, ProjectUpdate, VideoUpdate, UnitRecord

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['name', 'company', 'status', 'progress_pct', 'created_at']
    list_filter   = ['status']
    search_fields = ['name', 'company__name']

admin.site.register(ProjectMilestone)
admin.site.register(ProjectUpdate)
admin.site.register(VideoUpdate)
admin.site.register(UnitRecord)