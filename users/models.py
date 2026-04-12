from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models

from institutions.models import Institution


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        email = self.normalize_email(email)
        institution = Institution.get_or_create_from_email(email)
        user = self.model(
            email=email,
            name=name,
            institution=institution,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(unique=True, verbose_name="E-mail institucional")
    course = models.CharField(max_length=255, blank=True, verbose_name="Curso")
    bio = models.TextField(blank=True, verbose_name="Bio")
    avatar_url = models.URLField(blank=True, verbose_name="URL do avatar")
    skills = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        verbose_name="Habilidades"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Disponível para novos projetos"
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name="users",
        verbose_name="Instituição"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_user_groups',
        verbose_name="Grupos"
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_user_permissions',
        verbose_name="Permissões"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} <{self.email}>"