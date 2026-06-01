from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Project, VideoUpdate, UnitRecord, ProjectUpdate
from .serializers import (ProjectSerializer, ProjectListSerializer,
                           VideoUpdateSerializer, UnitRecordSerializer, UpdateSerializer)


class ProjectListView(generics.ListAPIView):
    serializer_class   = ProjectListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs         = Project.objects.filter(status='approved')
        company_id = self.request.query_params.get('company')
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs.select_related('company')


class ProjectCreateView(generics.CreateAPIView):
    serializer_class   = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        company = self.request.user.company
        serializer.save(company=company)


class ProjectDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if project.company.owner != request.user:
            return Response({'detail': 'İcazə yoxdur.'}, status=403)
        return super().update(request, *args, **kwargs)


class ProjectUpdateCreateView(generics.CreateAPIView):
    serializer_class   = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        serializer.save(project=project, created_by=self.request.user)


class VideoUploadView(APIView):
    parser_classes     = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        videos = VideoUpdate.objects.filter(project_id=pk)
        return Response(VideoUpdateSerializer(videos, many=True).data)

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.company.owner != request.user:
            return Response({'detail': 'İcazə yoxdur.'}, status=403)
        serializer = VideoUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, uploaded_by=request.user,
                        status='ready' if request.data.get('file') else 'pending')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnitLookupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        floor = request.query_params.get('floor')
        unit  = request.query_params.get('unit')
        qs    = UnitRecord.objects.filter(project_id=pk)
        if floor:
            qs = qs.filter(floor=floor)
        if unit:
            qs = qs.filter(unit=unit)
        return Response(UnitRecordSerializer(qs, many=True).data)