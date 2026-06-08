from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "app": "shaffaf-backend",
        "version": "2.1-production",
        "debug": settings.DEBUG,
        "environment": "production" if not settings.DEBUG else "development"
    })

urlpatterns = [
    path('', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/companies/', include('apps.companies.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/authority/', include('apps.authority.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)