from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Follow, SavedProject
from .serializers import UserFollowSerializer, SavedProjectSerializer
from users.models import User
from projects.models import Project


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        target = get_object_or_404(User, pk=pk)

        if target == request.user:
            return Response(
                {"detail": "Você não pode seguir a si mesmo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        _, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target
        )

        if not created:
            return Response(
                {"detail": "Você já segue este usuário."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": f"Você agora segue {target.name}."},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        follow = Follow.objects.filter(
            follower=request.user,
            following=target
        ).first()

        if not follow:
            return Response(
                {"detail": "Você não segue este usuário."},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowerListView(generics.ListAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return User.objects.filter(following__following=user)


class FollowingListView(generics.ListAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return User.objects.filter(followers__follower=user)


class SavedProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        _, created = SavedProject.objects.get_or_create(
            user=request.user,
            project=project
        )

        if not created:
            return Response(
                {"detail": "Projeto já está salvo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": f"Projeto '{project.title}' salvo com sucesso."},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        saved = SavedProject.objects.filter(
            user=request.user,
            project=project
        ).first()

        if not saved:
            return Response(
                {"detail": "Projeto não está salvo."},
                status=status.HTTP_400_BAD_REQUEST
            )

        saved.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedProjectListView(generics.ListAPIView):
    serializer_class = SavedProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedProject.objects.filter(user=self.request.user)