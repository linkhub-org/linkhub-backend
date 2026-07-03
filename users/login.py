from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers


class VerifiedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Chama a validação padrão do JWT
        data = super().validate(attrs)

        # Bloqueia login se e-mail não confirmado
        if not self.user.is_email_verified:
            raise serializers.ValidationError(
                "E-mail não confirmado. Verifique sua caixa de entrada."
            )

        return data


class VerifiedTokenObtainPairView(TokenObtainPairView):
    serializer_class = VerifiedTokenObtainPairSerializer