from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from .models import Company, CompanyDocument, CompanyReview
from .serializers import (CompanySerializer, CompanyListSerializer,
                           CompanyDocumentSerializer, CompanyReviewSerializer)
from .permissions import IsCompanyOwner


class CompanyListView(generics.ListAPIView):
    serializer_class   = CompanyListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs       = Company.objects.filter(status='approved')
        q        = self.request.query_params.get('q', '')
        category = self.request.query_params.get('category', '')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(location__icontains=q) |
                Q(specialties__icontains=q) | Q(description__icontains=q)
            )
        if category and category != 'all':
            qs = qs.filter(category=category)
        return qs


class CompanyRegisterView(generics.CreateAPIView):
    serializer_class   = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'company':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Yalnız developer/şirkət hesabı şirkət qeydiyyat edə bilər.')
        serializer.save(owner=self.request.user)


class CompanyDetailView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        return CompanySerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [IsCompanyOwner()]
        return [AllowAny()]


class CompanyDocumentUploadView(APIView):
    parser_classes     = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        company = Company.objects.get(pk=pk, owner=request.user)
        serializer = CompanyDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompanyReviewView(generics.ListCreateAPIView):
    serializer_class   = CompanyReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CompanyReview.objects.filter(company_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        company = Company.objects.get(pk=self.kwargs['pk'])
        serializer.save(company=company, author=self.request.user)
        reviews = company.reviews.all()
        company.rating       = sum(r.rating for r in reviews) / reviews.count()
        company.review_count = reviews.count()
        company.save(update_fields=['rating', 'review_count'])