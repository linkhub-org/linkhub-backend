from django.urls import path
from .views import NotificationListView, NotificationMarkReadView

urlpatterns = [
    # RF04.03 — Listar notificações
    path('notifications/', NotificationListView.as_view(), name='notification-list'),

    # RF04.04 — Marcar como lida
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-read'),
]