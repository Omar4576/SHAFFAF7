from django.contrib import admin
from .models import Company, CompanyDocument, CompanyReview

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'status', 'verified', 'plan', 'rating']
    list_filter   = ['status', 'category', 'plan', 'verified']
    search_fields = ['name', 'license_no']
    actions       = ['approve_companies']

    def approve_companies(self, request, queryset):
        queryset.update(status='approved', verified=True)
    approve_companies.short_description = "Seçilmişləri təsdiq et"

admin.site.register(CompanyDocument)
admin.site.register(CompanyReview)