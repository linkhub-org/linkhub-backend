from notifications.models import Notification, NotificationType


class NotificationService:

    @staticmethod
    def notify_new_application(application):
        Notification.objects.create(
            recipient=application.project.owner,
            type=NotificationType.NEW_APPLICATION,
            project=application.project,
            message=(
                f"{application.applicant.name} se candidatou ao seu projeto "
                f'"{application.project.title}".'
            )
        )

    @staticmethod
    def notify_application_result(application):
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
            project=application.project,
            message=message
        )