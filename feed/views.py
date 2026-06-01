from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter

from projects.models import Project, ProjectCategory, ProjectStatus
from projects.serializers import ProjectSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='category',
            description='Filtrar por categoria',
            required=False,
            type=str,
            enum=[c.value for c in ProjectCategory]
        ),
        OpenApiParameter(
            name='status',
            description='Filtrar por status',
            required=False,
            type=str,
            enum=[s.value for s in ProjectStatus]
        ),
    ]
)
class FeedView(generics.ListAPIView):
    """
    RF02.02 — GET /api/feed/
    Lista projetos da instituição do usuário em ordem cronológica
    decrescente, com filtros por category e status e busca por título.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = Project.objects.filter(
            institution=self.request.user.institution
        )

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset