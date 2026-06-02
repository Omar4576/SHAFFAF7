from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import RegisterView, LoginView, LogoutView, MeView, VerifyTokenView   # VerifyTokenView əlavə et

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/',    LoginView.as_view(),    name='auth-login'),
    path('logout/',   LogoutView.as_view(),   name='auth-logout'),
    path('refresh/',  TokenRefreshView.as_view(), name='auth-refresh'),
    path('me/',       MeView.as_view(),       name='auth-me'),
    path('verify/',   VerifyTokenView.as_view(), name='auth-verify'),   # ← Bu sətri əlavə et
]