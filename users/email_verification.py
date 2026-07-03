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


class EmailVerificationConfirmView(APIView):
    """
    GET /api/auth/verify-email/{uid}/{token}/
    Confirma o e-mail do usuário a partir do link enviado no cadastro.
    """
    permission_classes = [AllowAny]

    def get(self, request, uid, token):
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

        if user.is_email_verified:
            return Response(
                {"detail": "E-mail já confirmado. Faça login."},
                status=status.HTTP_200_OK
            )

        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        return Response(
            {"detail": "E-mail confirmado com sucesso! Agora você pode fazer login."},
            status=status.HTTP_200_OK
        )


class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResendVerificationEmailView(APIView):
    """
    POST /api/auth/resend-verification/
    Reenvia o e-mail de confirmação caso o usuário não tenha recebido.
    """
    permission_classes = [AllowAny]

    @extend_schema(request=ResendVerificationEmailSerializer)
    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            if not user.is_email_verified:
                send_verification_email(user)
        except User.DoesNotExist:
            pass

        return Response(
            {"detail": "Se este e-mail estiver cadastrado e não confirmado, você receberá um novo link."},
            status=status.HTTP_200_OK
        )


def send_verification_email(user):
    """
    Envia o e-mail de confirmação de cadastro.
    Chamado em RegisterView.perform_create().
    """
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.encoding import force_bytes
    from django.utils.http import urlsafe_base64_encode

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    frontend_url = config('FRONTEND_URL', default='http://localhost:5173')
    verify_link = f"{frontend_url}/verify-email/{uid}/{token}/"

    send_mail(
        subject="Confirme seu cadastro — Linkhub",
        message=(
            f"Olá, {user.name}!\n\n"
            f"Clique no link abaixo para confirmar seu e-mail e acessar o Linkhub:\n\n"
            f"{verify_link}\n\n"
            f"Se você não criou uma conta, ignore este e-mail."
        ),
        from_email="noreply@linkhub.com",
        recipient_list=[user.email],
    )