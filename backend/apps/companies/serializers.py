from rest_framework import serializers
from .models import Company, CompanyDocument, CompanyReview


class CompanyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CompanyDocument
        fields = ['id', 'doc_type', 'name', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class CompanyReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model  = CompanyReview
        fields = ['id', 'author_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'author_name', 'created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Reytinq 1-5 arasında olmalıdır.')
        return value


class CompanySerializer(serializers.ModelSerializer):
    documents     = CompanyDocumentSerializer(many=True, read_only=True)
    owner_email   = serializers.EmailField(source='owner.email', read_only=True)
    project_count = serializers.SerializerMethodField()

    class Meta:
        model  = Company
        fields = ['id', 'owner_email', 'name', 'category', 'description', 'location',
                  'founded_year', 'license_no', 'plan', 'status', 'verified',
                  'rating', 'review_count', 'specialties', 'logo', 'cover_color',
                  'documents', 'project_count', 'created_at']
        read_only_fields = ['id', 'status', 'verified', 'rating', 'review_count', 'created_at']

    def get_project_count(self, obj):
        return obj.projects.count()


class CompanyListSerializer(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()

    class Meta:
        model  = Company
        fields = ['id', 'name', 'category', 'location', 'founded_year',
                  'license_no', 'verified', 'rating', 'review_count',
                  'specialties', 'logo', 'cover_color', 'project_count']

    def get_project_count(self, obj):
        return obj.projects.count()