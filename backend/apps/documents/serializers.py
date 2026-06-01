from rest_framework import serializers
from .models import SignedDocument

class SignedDocumentSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)

    class Meta:
        model  = SignedDocument
        fields = ['id', 'owner_name', 'project', 'file_name', 'file',
                  'signer_name', 'signed_at', 'audit_id',
                  'signature_page', 'signature_x', 'signature_y']
        read_only_fields = ['id', 'owner_name', 'signed_at', 'audit_id']