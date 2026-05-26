from rest_framework import serializers
from .models import Project, ProjectStatus


class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'looking_for',
            'category', 'category_display',
            'status', 'status_display',
            'created_at', 'owner_name', 'institution_name'
        ]
        read_only_fields = ['id', 'created_at', 'owner_name', 'institution_name']

    def validate_status(self, value):
        # Impede criar projeto já com status encerrado
        if self.instance is None and value != ProjectStatus.OPEN:
            raise serializers.ValidationError(
                "Novos projetos devem ser criados com status Aberto."
            )
        return value