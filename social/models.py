from django.db import models
from users.models import User
from projects.models import Project


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name="Seguidor"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name="Seguido"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Seguimento"
        verbose_name_plural = "Seguimentos"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f"{self.follower.name} segue {self.following.name}"


class SavedProject(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_projects',
        verbose_name="Usuário"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='saved_by',
        verbose_name="Projeto"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Projeto Salvo"
        verbose_name_plural = "Projetos Salvos"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'],
                name='unique_saved_project'
            )
        ]

    def __str__(self):
        return f"{self.user.name} salvou {self.project.title}"