from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, UserMeView, UserPublicView, UserProjectsView
from .password_reset import PasswordResetRequestView, PasswordResetConfirmView
from .email_verification import EmailVerificationConfirmView, ResendVerificationEmailView
from .login import VerifiedTokenObtainPairView

urlpatterns = [
    # Cadastro
    path('auth/register/', RegisterView.as_view(), name='auth-register'),

    # Login — verifica e-mail confirmado
    path('auth/login/', VerifiedTokenObtainPairView.as_view(), name='auth-login'),

    # Tokens
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),

    # Verificação de e-mail
    path('auth/verify-email/<str:uid>/<str:token>/', EmailVerificationConfirmView.as_view(), name='auth-verify-email'),
    path('auth/resend-verification/', ResendVerificationEmailView.as_view(), name='auth-resend-verification'),

    # Recuperação de senha
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),

    # Perfil
    path('users/me/', UserMeView.as_view(), name='users-me'),
    path('users/me/projects/', UserProjectsView.as_view(), name='users-me-projects'),
    path('users/<int:pk>/', UserPublicView.as_view(), name='users-public'),
]