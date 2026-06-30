from rest_framework import serializers
from .models import Project, ProjectStatus

class MemberSerializer(serializers.Serializer):
    user_name = serializers.CharField(source='user.name')
    user_course = serializers.CharField(source='user.course')
    joined_at = serializers.DateTimeField()

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    saves_count = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'looking_for',
            'category', 'category_display',
            'status', 'status_display',
            'created_at', 'owner_name', 'institution_name',
            'members', 'saves_count', 'is_saved'
        ]
        read_only_fields = ['id', 'created_at', 'owner_name', 'institution_name']

    def get_saves_count(self, obj):
        return obj.saved_by.count()

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(user=request.user).exists()
        return False

    def validate_status(self, value):
        if self.instance is None and value != ProjectStatus.OPEN:
            raise serializers.ValidationError(
                "Novos projetos devem ser criados com status Aberto."
            )
        return value