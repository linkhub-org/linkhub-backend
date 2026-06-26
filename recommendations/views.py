# recommendations/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from projects.models import Project
from applications.models import ProjectMember
from users.models import User

from .services import recommend_profiles_for_project, recommend_projects_for_user


class RecommendProfilesView(APIView):
    """
    GET /api/projects/{id}/recommend-profiles/
    Retorna perfis recomendados para um projeto.
    Visível apenas para o criador do projeto.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        # Busca o projeto garantindo que é da instituição do usuário
        try:
            project = Project.objects.get(
                id=project_id,
                institution=request.user.institution
            )
        except Project.DoesNotExist:
            raise NotFound("Projeto não encontrado.")

        # Apenas o criador pode ver as recomendações
        if project.owner != request.user:
            raise PermissionDenied("Apenas o criador do projeto pode ver recomendações.")

        # IDs dos membros atuais do projeto (inclui o próprio dono)
        member_ids = ProjectMember.objects.filter(
            project=project
        ).values_list('user_id', flat=True)

        # Perfis disponíveis: mesma instituição, ativo, disponível, fora do projeto
        available_profiles = User.objects.filter(
            institution=request.user.institution,
            is_active=True,
            is_available=True,
        ).exclude(
            id__in=member_ids
        ).exclude(
            id=project.owner.id
        )

        if not available_profiles.exists():
            return Response([])

        recommendations = recommend_profiles_for_project(project, available_profiles)
        return Response(recommendations)


class RecommendProjectsView(APIView):
    """
    GET /api/users/me/recommend-projects/
    Retorna projetos recomendados para o usuário autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # IDs dos projetos que o usuário já participa ou criou
        member_project_ids = ProjectMember.objects.filter(
            user=user
        ).values_list('project_id', flat=True)

        owned_project_ids = Project.objects.filter(
            owner=user
        ).values_list('id', flat=True)

        # Projetos disponíveis: mesma instituição, abertos, fora dos que já participa
        available_projects = Project.objects.filter(
            institution=user.institution,
            status='open',
        ).exclude(
            id__in=member_project_ids
        ).exclude(
            id__in=owned_project_ids
        )

        if not available_projects.exists():
            return Response([])

        recommendations = recommend_projects_for_user(user, available_projects)
        return Response(recommendations)