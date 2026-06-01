from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter

from projects.models import Project
from projects.serializers import ProjectSerializer


class FeedView(generics.ListAPIView):
    """
    RF02.02 — GET /api/feed/
    Lista projetos da instituição do usuário em ordem cronológica
    decrescente, com filtros por category e status e busca por título.

    Parâmetros opcionais:
        ?category=STARTUP
        ?status=OPEN
        ?search=nome-do-projeto
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = Project.objects.filter(
            institution=self.request.user.institution
        )

        # Filtro por categoria
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        # Filtro por status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        return queryset