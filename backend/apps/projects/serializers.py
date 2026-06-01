from rest_framework import serializers
from .models import Project, ProjectMilestone, ProjectUpdate, VideoUpdate, UnitRecord


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProjectMilestone
        fields = ['id', 'name', 'done', 'target_date', 'pct']


class UpdateSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model  = ProjectUpdate
        fields = ['id', 'text', 'author', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class VideoUpdateSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)

    class Meta:
        model  = VideoUpdate
        fields = ['id', 'title', 'area', 'video_type', 'status', 'duration',
                  'file', 'uploaded_by_name', 'created_at']
        read_only_fields = ['id', 'uploaded_by_name', 'created_at']


class UnitRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UnitRecord
        fields = ['id', 'floor', 'unit', 'unit_type', 'status', 'ready',
                  'latest_video', 'notes', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    milestones   = MilestoneSerializer(many=True, read_only=True)
    updates      = UpdateSerializer(many=True, read_only=True)
    videos       = VideoUpdateSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_id   = serializers.UUIDField(source='company.id', read_only=True)

    class Meta:
        model  = Project
        fields = ['id', 'company_id', 'company_name', 'name', 'description', 'location',
                  'status', 'progress_pct', 'total_floors', 'completed_floors',
                  'total_units', 'handover_date', 'cover_color',
                  'supplier', 'materials_info',
                  'milestones', 'updates', 'videos', 'created_at']
        read_only_fields = ['id', 'status', 'company_id', 'company_name', 'created_at']


class ProjectListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model  = Project
        fields = ['id', 'company_name', 'name', 'location', 'status',
                  'progress_pct', 'total_floors', 'completed_floors',
                  'total_units', 'handover_date', 'cover_color', 'created_at']