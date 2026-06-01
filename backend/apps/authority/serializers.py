from rest_framework import serializers
from .models import AuthorityReview, AuthorityNote


class AuthorityNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model  = AuthorityNote
        fields = ['id', 'author_name', 'text', 'created_at']
        read_only_fields = ['id', 'author_name', 'created_at']


class AuthorityReviewSerializer(serializers.ModelSerializer):
    project_name  = serializers.CharField(source='project.name', read_only=True)
    company_name  = serializers.CharField(source='project.company.name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)
    notes_list    = AuthorityNoteSerializer(source='note_list', many=True, read_only=True)

    class Meta:
        model  = AuthorityReview
        fields = ['id', 'project', 'project_name', 'company_name',
                  'reviewer_name', 'decision', 'notes', 'notes_list',
                  'reviewed_at', 'created_at']
        read_only_fields = ['id', 'project_name', 'company_name',
                            'reviewer_name', 'reviewed_at', 'created_at']