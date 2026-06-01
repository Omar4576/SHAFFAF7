from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import AuthorityReview, AuthorityNote
from .serializers import AuthorityReviewSerializer, AuthorityNoteSerializer
from .permissions import IsAuthorityUser
from apps.projects.models import Project


class AuthorityProjectListView(generics.ListAPIView):
    serializer_class   = AuthorityReviewSerializer
    permission_classes = [IsAuthorityUser]

    def get_queryset(self):
        decision = self.request.query_params.get('decision', 'pending')
        return AuthorityReview.objects.filter(decision=decision).select_related(
            'project', 'project__company', 'reviewer')


class AuthorityReviewDetailView(APIView):
    permission_classes = [IsAuthorityUser]

    def patch(self, request, pk):
        review   = get_object_or_404(AuthorityReview, project_id=pk)
        decision = request.data.get('decision')
        notes    = request.data.get('notes', '')

        if decision not in ('approved', 'changes', 'rejected'):
            return Response({'detail': 'Yanlış qərar dəyəri.'}, status=400)

        review.decision    = decision
        review.notes       = notes
        review.reviewer    = request.user
        review.reviewed_at = timezone.now()
        review.save()

        project = review.project
        if decision == 'approved':
            project.status = 'approved'
        elif decision == 'rejected':
            project.status = 'rejected'
        else:
            project.status = 'pending'
        project.save(update_fields=['status'])

        return Response(AuthorityReviewSerializer(review).data)


class AuthorityNoteView(generics.CreateAPIView):
    serializer_class   = AuthorityNoteSerializer
    permission_classes = [IsAuthorityUser]

    def perform_create(self, serializer):
        review = get_object_or_404(AuthorityReview, project_id=self.kwargs['pk'])
        serializer.save(review=review, author=self.request.user)