from django.db import models
from users.models import User
from institutions.models import Institution


class ProjectStatus(models.TextChoices):
    OPEN = 'open', 'Aberto'
    IN_PROGRESS = 'in_progress', 'Em andamento'
    COMPLETED = 'completed', 'Concluído'
    CANCELLED = 'cancelled', 'Cancelado'


class ProjectCategory(models.TextChoices):
    ACADEMIC = 'academic', 'Acadêmico'
    STARTUP = 'startup', 'Startup'
    OPEN_SOURCE = 'open_source', 'Open Source'
    SOCIAL = 'social', 'Social'
    OTHER = 'other', 'Outros'


class Project(models.Model):
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(verbose_name="Descrição")
    looking_for = models.TextField(verbose_name="Perfil buscado")
    category = models.CharField(
        max_length=20,
        choices=ProjectCategory.choices,
        verbose_name="Categoria"
    )
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.OPEN,
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="Criador"
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name="Instituição"
    )

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"