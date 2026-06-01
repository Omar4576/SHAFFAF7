from django.urls import path
from .views import AuthorityProjectListView, AuthorityReviewDetailView, AuthorityNoteView

urlpatterns = [
    path('projects/',                  AuthorityProjectListView.as_view(), name='authority-list'),
    path('projects/<uuid:pk>/',        AuthorityReviewDetailView.as_view(),name='authority-review'),
    path('projects/<uuid:pk>/notes/',  AuthorityNoteView.as_view(),        name='authority-notes'),
]