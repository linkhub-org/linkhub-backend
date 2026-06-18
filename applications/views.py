from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Application, ApplicationStatus, ProjectMember
from .serializers import ApplicationSerializer, ApplicationStatusUpdateSerializer, ProjectMemberSerializer
from projects.models import Project
from notifications.services import NotificationService


class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = get_object_or_404(
            Project, pk=self.kwargs['project_pk']
        )
        return context

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        application = serializer.save(
            applicant=self.request.user,
            project=project
        )
        # RF04.01 — Notifica o criador do projeto
        NotificationService.notify_new_application(application)


class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])

        # Apenas o criador pode ver as candidaturas
        if project.owner != self.request.user:
            raise PermissionDenied(
                "Apenas o criador do projeto pode ver as candidaturas."
            )
        return Application.objects.filter(project=project)


class ApplicationUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            project__owner=self.request.user
        )

    def perform_update(self, serializer):
        application = self.get_object()
        serializer.save()

        # Se aceito, cria o ProjectMember automaticamente
        if serializer.validated_data['status'] == ApplicationStatus.ACCEPTED:
            ProjectMember.objects.get_or_create(
                project=application.project,
                user=application.applicant
            )

        # RF04.02 — Notifica o candidato sobre o resultado
        application.refresh_from_db()
        NotificationService.notify_application_result(application)


class ApplicationDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)

    def perform_destroy(self, instance):
        # Apenas candidaturas pendentes podem ser canceladas
        if instance.status != ApplicationStatus.PENDING:
            raise ValidationError(
                "Apenas candidaturas pendentes podem ser canceladas."
            )
        instance.delete()