from rest_framework import generics, permissions
from rest_framework.response import Response

from projects.models import Project
from projects.serializers import ProjectSerializer
from .models import User
from .serializers import RegisterSerializer, UserMeSerializer, UserPublicSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserPublicView(generics.RetrieveAPIView):
    """
    RF01.06 — GET /api/users/{id}/
    Visualizar perfil público de outro usuário da mesma instituição.
    Requer autenticação.
    """
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Garante isolamento: só retorna usuários da mesma instituição
        # Exclui o próprio usuário — para isso use /api/users/me/
        return User.objects.filter(
            institution=self.request.user.institution
        ).exclude(pk=self.request.user.pk)



class UserProjectsView(generics.ListAPIView):
    """
    GET /api/users/me/projects/
    Retorna os projetos criados e os projetos em que o usuário é membro.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Projetos criados pelo usuário
        owned = Project.objects.filter(owner=user)

        # Projetos em que é membro
        member_of = Project.objects.filter(
            members__user=user
        ).exclude(owner=user)

        # Une os dois querysets
        from itertools import chain
        from django.db.models import QuerySet
        combined_ids = list(owned.values_list('id', flat=True)) + \
                       list(member_of.values_list('id', flat=True))
        return Project.objects.filter(id__in=combined_ids).order_by('-created_at')