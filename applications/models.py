from django.db import models
from users.models import User
from projects.models import Project, ProjectStatus


class ApplicationStatus(models.TextChoices):
    PENDING = 'pending', 'Pendente'
    ACCEPTED = 'accepted', 'Aceito'
    REJECTED = 'rejected', 'Recusado'


class Application(models.Model):
    message = models.TextField(verbose_name="Mensagem de apresentação")
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name="Candidato"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name="Projeto"
    )

    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['applicant', 'project'],
                name='unique_application_per_user_per_project'
            )
        ]

    def __str__(self):
        return f"{self.applicant.name} → {self.project.title} ({self.get_status_display()})"


class ProjectMember(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name="Projeto"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name="Membro"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Membro do Projeto"
        verbose_name_plural = "Membros do Projeto"
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user.name} em {self.project.title}"