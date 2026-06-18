from django.db import models

from users.models import User


class NotificationType(models.TextChoices):
    NEW_APPLICATION = "NEW_APPLICATION", "Nova candidatura recebida"
    APPLICATION_ACCEPTED = "APPLICATION_ACCEPTED", "Candidatura aceita"
    APPLICATION_REJECTED = "APPLICATION_REJECTED", "Candidatura recusada"


class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Destinatário"
    )
    type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        verbose_name="Tipo"
    )
    message = models.TextField(verbose_name="Mensagem")
    is_read = models.BooleanField(default=False, verbose_name="Lida")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.type}] → {self.recipient.name}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=["is_read"])