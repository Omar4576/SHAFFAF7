from django.urls import path
from .views import (ProjectListView, ProjectCreateView, ProjectDetailView,
                    VideoUploadView, UnitLookupView, ProjectUpdateCreateView)

urlpatterns = [
    path('',                       ProjectListView.as_view(),        name='project-list'),
    path('create/',                ProjectCreateView.as_view(),      name='project-create'),
    path('<uuid:pk>/',             ProjectDetailView.as_view(),      name='project-detail'),
    path('<uuid:pk>/updates/',     ProjectUpdateCreateView.as_view(),name='project-updates'),
    path('<uuid:pk>/videos/',      VideoUploadView.as_view(),        name='project-videos'),
    path('<uuid:pk>/units/',       UnitLookupView.as_view(),         name='project-units'),
]