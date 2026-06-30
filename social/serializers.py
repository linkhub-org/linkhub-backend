from rest_framework import serializers
from .models import Follow, SavedProject
from users.models import User
from projects.models import Project


class FollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.CharField(source='follower.name', read_only=True)
    following_name = serializers.CharField(source='following.name', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower_name', 'following_name', 'created_at']
        read_only_fields = ['id', 'follower_name', 'following_name', 'created_at']


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'course', 'bio', 'avatar_url', 'is_available']


class SavedProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='project.title', read_only=True)
    description = serializers.CharField(source='project.description', read_only=True)
    category_display = serializers.CharField(source='project.get_category_display', read_only=True)
    status_display = serializers.CharField(source='project.get_status_display', read_only=True)
    status = serializers.CharField(source='project.status', read_only=True)
    owner_name = serializers.CharField(source='project.owner.name', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)

    class Meta:
        model = SavedProject
        fields = [
            'id', 'project_id', 'title', 'description',
            'category_display', 'status', 'status_display',
            'owner_name', 'created_at'
        ]
        read_only_fields = fields