from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from institutions.models import Institution
from users.models import User
from projects.models import Project, ProjectStatus
from .models import Application, ApplicationStatus, ProjectMember


class ApplicationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.institution = Institution.objects.create(
            name="UFRN",
            email_domain="ufrn.edu.br"
        )

        self.owner = User.objects.create_user(
            email="kaio@ufrn.edu.br",
            name="Kaio Lira",
            password="Senha@123",
            course="Sistemas de Informação"
        )

        self.applicant = User.objects.create_user(
            email="guilherme@ufrn.edu.br",
            name="Guilherme Dev",
            password="Senha@123",
            course="Ciência da Computação"
        )

        self.project = Project.objects.create(
            title="App de Estudos",
            description="Aplicativo mobile para estudantes",
            looking_for="Desenvolvedor mobile",
            category="academic",
            owner=self.owner,
            institution=self.institution
        )

        self.apply_url = reverse('application-create', kwargs={'project_pk': self.project.pk})
        self.list_url = reverse('application-list', kwargs={'project_pk': self.project.pk})

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # TA03.01 — Candidatura bem-sucedida
    def test_create_application_success(self):
        self.authenticate(self.applicant)
        response = self.client.post(self.apply_url, {"message": "Quero participar!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], ApplicationStatus.PENDING)
        self.assertEqual(response.data['applicant_name'], "Guilherme Dev")

    # TA03.02 — Candidatura sem mensagem
    def test_create_application_missing_message(self):
        self.authenticate(self.applicant)
        response = self.client.post(self.apply_url, {"message": ""}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

    # TA03.03 — Segunda candidatura ao mesmo projeto
    def test_create_duplicate_application(self):
        self.authenticate(self.applicant)
        self.client.post(self.apply_url, {"message": "Primeira candidatura"}, format='json')
        response = self.client.post(self.apply_url, {"message": "Segunda candidatura"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TA03.04 — Criador tenta se candidatar ao próprio projeto
    def test_owner_cannot_apply(self):
        self.authenticate(self.owner)
        response = self.client.post(self.apply_url, {"message": "Quero entrar!"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TA03.05 — Criador aceita candidatura e ProjectMember é criado
    def test_accept_application_creates_member(self):
        self.authenticate(self.applicant)
        self.client.post(self.apply_url, {"message": "Quero participar!"}, format='json')

        application = Application.objects.get(applicant=self.applicant, project=self.project)
        update_url = reverse('application-update', kwargs={'pk': application.pk})

        self.authenticate(self.owner)
        response = self.client.patch(update_url, {"status": "accepted"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], ApplicationStatus.ACCEPTED)
        self.assertTrue(ProjectMember.objects.filter(
            project=self.project,
            user=self.applicant
        ).exists())

    # TA03.06 — Criador recusa candidatura
    def test_reject_application(self):
        self.authenticate(self.applicant)
        self.client.post(self.apply_url, {"message": "Quero participar!"}, format='json')

        application = Application.objects.get(applicant=self.applicant, project=self.project)
        update_url = reverse('application-update', kwargs={'pk': application.pk})

        self.authenticate(self.owner)
        response = self.client.patch(update_url, {"status": "rejected"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], ApplicationStatus.REJECTED)

    # TA03.07 — Candidato cancela candidatura pendente
    def test_cancel_pending_application(self):
        self.authenticate(self.applicant)
        self.client.post(self.apply_url, {"message": "Quero participar!"}, format='json')

        application = Application.objects.get(applicant=self.applicant, project=self.project)
        cancel_url = reverse('application-delete', kwargs={'pk': application.pk})

        response = self.client.delete(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Application.objects.filter(pk=application.pk).exists())

    # TA03.08 — Cancelar candidatura já aceita
    def test_cannot_cancel_accepted_application(self):
        self.authenticate(self.applicant)
        self.client.post(self.apply_url, {"message": "Quero participar!"}, format='json')

        application = Application.objects.get(applicant=self.applicant, project=self.project)
        update_url = reverse('application-update', kwargs={'pk': application.pk})
        cancel_url = reverse('application-delete', kwargs={'pk': application.pk})

        self.authenticate(self.owner)
        self.client.patch(update_url, {"status": "accepted"}, format='json')

        self.authenticate(self.applicant)
        response = self.client.delete(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)