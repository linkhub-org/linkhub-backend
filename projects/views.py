from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Project, ProjectStatus
from .serializers import ProjectSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category']

    def get_queryset(self):
        # Filtra apenas projetos da mesma instituição do usuário
        queryset = Project.objects.filter(
            institution=self.request.user.institution
        )
        # Filtro opcional por status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filtro opcional por categoria
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def perform_create(self, serializer):
        # Define owner e institution automaticamente pelo usuário logado
        serializer.save(
            owner=self.request.user,
            institution=self.request.user.institution
        )


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            institution=self.request.user.institution
        )

    def perform_update(self, serializer):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied("Apenas o criador pode editar este projeto.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Apenas o criador pode excluir este projeto.")
        instance.delete()