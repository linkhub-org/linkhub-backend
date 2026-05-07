from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer, UserMeSerializer, UserPublicSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserPublicView(generics.RetrieveAPIView):

    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Garante isolamento: só retorna usuários da mesma instituição
        return User.objects.filter(
            institution=self.request.user.institution
        )