from django.contrib import admin
from .models import SignedDocument

@admin.register(SignedDocument)
class SignedDocumentAdmin(admin.ModelAdmin):
    list_display   = ['file_name', 'signer_name', 'audit_id', 'signed_at']
    search_fields  = ['audit_id', 'signer_name']
    readonly_fields = ['audit_id']