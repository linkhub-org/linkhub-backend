from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    RF04.03 — GET /api/notifications/
    Lista as notificações do usuário autenticado
    em ordem cronológica decrescente.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        )


class NotificationMarkReadView(APIView):
    """
    RF04.04 — PATCH /api/notifications/{id}/read/
    Marca uma notificação como lida.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(
                pk=pk,
                recipient=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Notificação não encontrada."},
                status=404
            )

        notification.mark_as_read()
        return Response(NotificationSerializer(notification).data)