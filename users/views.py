from rest_framework import generics, permissions
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer
from .models import User
from .serializers import RegisterSerializer, UserMeSerializer, UserPublicSerializer
from .email_verification import send_verification_email


class RegisterView(generics.CreateAPIView):
    """
    RF01.01 — POST /api/auth/register/
    Cadastro de novo usuário com e-mail institucional.
    Não requer autenticação.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Envia e-mail de confirmação após cadastro
        send_verification_email(user)


class UserMeView(generics.RetrieveUpdateAPIView):
    """
    RF01.04 — GET /api/users/me/
    RF01.05 — PUT /api/users/me/
    """
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserPublicView(generics.RetrieveAPIView):
    """
    RF01.06 — GET /api/users/{id}/
    """
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            institution=self.request.user.institution
        ).exclude(pk=self.request.user.pk)


class UserProjectsView(generics.ListAPIView):
    """
    GET /api/users/me/projects/
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        owned = Project.objects.filter(owner=user)
        member_of = Project.objects.filter(
            members__user=user
        ).exclude(owner=user)
        combined_ids = (
            list(owned.values_list('id', flat=True)) +
            list(member_of.values_list('id', flat=True))
        )
        return Project.objects.filter(id__in=combined_ids).order_by('-created_at')