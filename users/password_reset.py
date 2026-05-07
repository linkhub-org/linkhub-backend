from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetRequestView(APIView):
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
            reset_link = f"http://localhost:5173/reset-password/{uid}/{token}/"

            send_mail(
                subject="Recuperação de senha — Linkhub",
                message=f"Clique no link para redefinir sua senha:\n\n{reset_link}",
                from_email="noreply@linkhub.com",
                recipient_list=[email],
            )
        except User.DoesNotExist:
            pass

        return Response(
            {"detail": "Se este e-mail estiver cadastrado, você receberá as instruções em breve."},
            status=status.HTTP_200_OK
        )