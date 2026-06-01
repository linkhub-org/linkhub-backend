from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from users.models import User
from projects.models import Project
from applications.models import Application
from notifications.models import Notification, NotificationType


def create_user(email, name="Usuário"):
    return User.objects.create_user(
        email=email,
        name=name,
        password="Senha@1234",
        course="Computação"
    )

def create_project(owner, title="Projeto Teste", category="academic"):
    return Project.objects.create(
        title=title,
        description="Descrição",
        looking_for="Desenvolvedor",
        category=category,
        status="open",
        owner=owner,
        institution=owner.institution
    )

def login(client, email):
    response = client.post('/api/auth/login/', {
        'email': email,
        'password': 'Senha@1234'
    })
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")


class NotificationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.owner = create_user('owner@ufrn.br', 'Dono')
        self.applicant = create_user('applicant@ufrn.br', 'Candidato')
        self.project = create_project(self.owner)

    # TA05.01 — Notificação gerada ao receber candidatura
    def test_notify_owner_on_new_application(self):
        login(self.client, 'applicant@ufrn.br')
        self.client.post(f'/api/projects/{self.project.pk}/apply/', {
            'message': 'Quero participar!'
        })
        notification = Notification.objects.filter(
            recipient=self.owner,
            type=NotificationType.NEW_APPLICATION
        )
        self.assertTrue(notification.exists())

    # TA05.02 — Notificação gerada ao aceitar candidatura
    def test_notify_applicant_on_accept(self):
        login(self.client, 'applicant@ufrn.br')
        self.client.post(f'/api/projects/{self.project.pk}/apply/', {
            'message': 'Quero participar!'
        })
        application = Application.objects.get(
            applicant=self.applicant,
            project=self.project
        )
        login(self.client, 'owner@ufrn.br')
        self.client.patch(f'/api/applications/{application.pk}/', {
            'status': 'accepted'
        })
        notification = Notification.objects.filter(
            recipient=self.applicant,
            type=NotificationType.APPLICATION_ACCEPTED
        )
        self.assertTrue(notification.exists())

    # TA05.03 — Notificação gerada ao recusar candidatura
    def test_notify_applicant_on_reject(self):
        login(self.client, 'applicant@ufrn.br')
        self.client.post(f'/api/projects/{self.project.pk}/apply/', {
            'message': 'Quero participar!'
        })
        application = Application.objects.get(
            applicant=self.applicant,
            project=self.project
        )
        login(self.client, 'owner@ufrn.br')
        self.client.patch(f'/api/applications/{application.pk}/', {
            'status': 'rejected'
        })
        notification = Notification.objects.filter(
            recipient=self.applicant,
            type=NotificationType.APPLICATION_REJECTED
        )
        self.assertTrue(notification.exists())

    # TA05.04/05 — Marcar notificação como lida
    def test_mark_notification_as_read(self):
        login(self.client, 'applicant@ufrn.br')
        self.client.post(f'/api/projects/{self.project.pk}/apply/', {
            'message': 'Quero participar!'
        })
        notification = Notification.objects.get(recipient=self.owner)
        login(self.client, 'owner@ufrn.br')
        response = self.client.patch(f'/api/notifications/{notification.pk}/read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    # TA05.06 — Notificações ordenadas da mais recente para a mais antiga
    def test_notifications_ordered_by_created_at(self):
        login(self.client, 'applicant@ufrn.br')
        self.client.post(f'/api/projects/{self.project.pk}/apply/', {
            'message': 'Quero participar!'
        })
        project2 = create_project(self.owner, title="Projeto 2")
        applicant2 = create_user('applicant2@ufrn.br', 'Candidato 2')
        login(self.client, 'applicant2@ufrn.br')
        self.client.post(f'/api/projects/{project2.pk}/apply/', {
            'message': 'Quero participar!'
        })
        login(self.client, 'owner@ufrn.br')
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dates = [n['created_at'] for n in response.data]
        self.assertEqual(dates, sorted(dates, reverse=True))