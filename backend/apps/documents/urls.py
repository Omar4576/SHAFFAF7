from django.urls import path
from .views import DocumentListView, DocumentSignView, DocumentVerifyView

urlpatterns = [
    path('',                       DocumentListView.as_view(),  name='document-list'),
    path('sign/',                  DocumentSignView.as_view(),  name='document-sign'),
    path('verify/<str:audit_id>/', DocumentVerifyView.as_view(),name='document-verify'),
]