from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import SignedDocument
from .serializers import SignedDocumentSerializer


class DocumentListView(generics.ListAPIView):
    serializer_class   = SignedDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SignedDocument.objects.filter(owner=self.request.user)


class DocumentSignView(APIView):
    parser_classes     = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SignedDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DocumentVerifyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, audit_id):
        doc = get_object_or_404(SignedDocument, audit_id=audit_id)
        return Response({
            'valid':       True,
            'audit_id':    doc.audit_id,
            'file_name':   doc.file_name,
            'signer_name': doc.signer_name,
            'signed_at':   doc.signed_at,
            'project':     str(doc.project) if doc.project else None,
        })