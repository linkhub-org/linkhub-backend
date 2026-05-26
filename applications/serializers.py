from rest_framework import serializers
from .models import Application, ApplicationStatus, ProjectMember
from projects.models import ProjectStatus


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.name', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'message', 'status', 'status_display',
            'created_at', 'applicant_name', 'project_title'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'applicant_name', 'project_title']

    def validate(self, data):
        request = self.context['request']
        project = self.context['project']

        # Valida que o candidato não é o criador do projeto
        if project.owner == request.user:
            raise serializers.ValidationError(
                "O criador do projeto não pode se candidatar ao próprio projeto."
            )

        # Valida que o projeto está aberto
        if project.status != ProjectStatus.OPEN:
            raise serializers.ValidationError(
                "Não é possível se candidatar a um projeto que não está aberto."
            )

        # Valida candidatura duplicada
        if Application.objects.filter(applicant=request.user, project=project).exists():
            raise serializers.ValidationError(
                "Você já se candidatou a este projeto."
            )

        return data


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']

    def validate_status(self, value):
        # Só permite aceitar ou recusar
        if value not in [ApplicationStatus.ACCEPTED, ApplicationStatus.REJECTED]:
            raise serializers.ValidationError(
                "Status inválido. Use 'accepted' ou 'rejected'."
            )
        return value


class ProjectMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_course = serializers.CharField(source='user.course', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'user_name', 'user_course', 'joined_at']