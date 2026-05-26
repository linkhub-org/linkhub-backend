from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from decouple import config

from .models import User


# ── Serializers ────────────────────────────────────────────────────────────────

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)


# ── Views ──────────────────────────────────────────────────────────────────────

class PasswordResetRequestView(APIView):
    """
    RF01.03 — POST /api/auth/password-reset/
    Envia e-mail com link de recuperação de senha.
    """
    permission_classes = [AllowAny]

    @extend_schema(request=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # ⚠️ FRONTEND_URL via variável de ambiente — não hardcoded
            frontend_url = config('FRONTEND_URL', default='http://localhost:5173')
            reset_link = f"{frontend_url}/reset-password/{uid}/{token}/"

            send_mail(
                subject="Recuperação de senha — Linkhub",
                message=f"Clique no link para redefinir sua senha:\n\n{reset_link}",
                from_email="noreply@linkhub.com",
                recipient_list=[email],
            )
        except User.DoesNotExist:
            # Não revelamos se o e-mail existe ou não por segurança
            pass

        return Response(
            {"detail": "Se este e-mail estiver cadastrado, você receberá as instruções em breve."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    """
    RF01.03 — POST /api/auth/password-reset/confirm/
    Valida o token e redefine a senha do usuário.
    """
    permission_classes = [AllowAny]

    @extend_schema(request=PasswordResetConfirmSerializer)
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"detail": "Link inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Link inválido ou expirado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Senha redefinida com sucesso."},
            status=status.HTTP_200_OK
        )