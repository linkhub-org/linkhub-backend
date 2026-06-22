from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, UserMeView, UserPublicView
from .password_reset import PasswordResetRequestView, PasswordResetConfirmView
from .views import RegisterView, UserMeView, UserPublicView, UserProjectsView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    path('users/me/', UserMeView.as_view(), name='users-me'),
    path('users/<int:pk>/', UserPublicView.as_view(), name='users-public'),
    path('users/me/projects/', UserProjectsView.as_view(), name='users-me-projects'),
]