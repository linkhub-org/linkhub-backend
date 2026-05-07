from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from institutions.models import Institution
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'course']

    def validate_email(self, value):
        blocked_domains = [
            'gmail.com', 'hotmail.com', 'yahoo.com',
            'outlook.com', 'live.com', 'icloud.com'
        ]
        domain = value.split('@')[-1]
        if domain in blocked_domains:
            raise serializers.ValidationError(
                "Apenas e-mails institucionais são permitidos."
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            course=validated_data.get('course', '')
        )
        return user


class UserPublicSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(
        source='institution.name',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'name', 'course', 'bio',
            'avatar_url', 'skills', 'is_available',
            'institution_name'
        ]


class UserMeSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(
        source='institution.name',
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'course', 'bio',
            'avatar_url', 'skills', 'is_available',
            'institution_name'
        ]
        read_only_fields = ['id', 'email', 'institution_name']