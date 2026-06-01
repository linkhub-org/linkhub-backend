from notifications.models import Notification, NotificationType


class NotificationService:
    """
    Serviço de notificações síncronas.
    Geradas na mesma transação do evento — sem Celery ou Redis.
    """

    @staticmethod
    def notify_new_application(application):
        """
        RF04.01 — Notifica o criador ao receber uma nova candidatura.
        Chamado em ApplicationCreateView.perform_create().
        """
        Notification.objects.create(
            recipient=application.project.owner,
            type=NotificationType.NEW_APPLICATION,
            message=(
                f"{application.applicant.name} se candidatou ao seu projeto "
                f'"{application.project.title}".'
            )
        )

    @staticmethod
    def notify_application_result(application):
        """
        RF04.02 — Notifica o candidato sobre o resultado.
        Chamado em ApplicationUpdateView.perform_update().
        """
        # Atenção: valores em minúsculo conforme implementação do Kaio
        if application.status == "accepted":
            ntype = NotificationType.APPLICATION_ACCEPTED
            message = (
                f'Sua candidatura ao projeto '
                f'"{application.project.title}" foi aceita!'
            )
        else:
            ntype = NotificationType.APPLICATION_REJECTED
            message = (
                f'Sua candidatura ao projeto '
                f'"{application.project.title}" foi recusada.'
            )

        Notification.objects.create(
            recipient=application.applicant,
            type=ntype,
            message=message
        )