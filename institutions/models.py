from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    email_domain = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Domínio de e-mail",
        help_text="Ex: ufrn.edu.br"
    )

    class Meta:
        verbose_name = "Instituição"
        verbose_name_plural = "Instituições"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.email_domain})"

    @classmethod
    def get_or_create_from_email(cls, email: str):
        """
        Extrai o domínio do e-mail e retorna (ou cria)
        a instituição correspondente.
        Chamado automaticamente no cadastro do usuário.
        """
        domain = email.split("@")[-1]
        institution, _ = cls.objects.get_or_create(
            email_domain=domain,
            defaults={"name": domain}
        )
        return institution