from django.urls import path
from .views import (CompanyListView, CompanyRegisterView, CompanyDetailView,
                    CompanyDocumentUploadView, CompanyReviewView)

urlpatterns = [
    path('',                     CompanyListView.as_view(),           name='company-list'),
    path('register/',            CompanyRegisterView.as_view(),       name='company-register'),
    path('<uuid:pk>/',           CompanyDetailView.as_view(),         name='company-detail'),
    path('<uuid:pk>/documents/', CompanyDocumentUploadView.as_view(), name='company-docs'),
    path('<uuid:pk>/reviews/',   CompanyReviewView.as_view(),         name='company-reviews'),
]