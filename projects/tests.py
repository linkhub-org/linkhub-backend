from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from institutions.models import Institution
from users.models import User
from .models import Project, ProjectStatus, ProjectCategory


class ProjectTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Instituição UFRN
        self.institution_ufrn = Institution.objects.create(
            name="UFRN",
            email_domain="ufrn.edu.br"
        )

        # Instituição UFPB
        self.institution_ufpb = Institution.objects.create(
            name="UFPB",
            email_domain="ufpb.edu.br"
        )

        # Usuário criador (UFRN)
        self.owner = User.objects.create_user(
            email="kaio@ufrn.edu.br",
            name="Kaio Lira",
            password="Senha@123",
            course="Sistemas de Informação"
        )

        # Usuário da mesma instituição (UFRN)
        self.other_user = User.objects.create_user(
            email="guilherme@ufrn.edu.br",
            name="Guilherme Dev",
            password="Senha@123",
            course="Ciência da Computação"
        )

        # Usuário de outra instituição (UFPB)
        self.ufpb_user = User.objects.create_user(
            email="estudante@ufpb.edu.br",
            name="Estudante UFPB",
            password="Senha@123",
            course="Engenharia"
        )

        # Projeto base
        self.project = Project.objects.create(
            title="Linkhub Frontend",
            description="Desenvolvimento do frontend em React",
            looking_for="Desenvolvedor React",
            category=ProjectCategory.OPEN_SOURCE,
            owner=self.owner,
            institution=self.institution_ufrn
        )

        self.list_url = reverse('project-list-create')
        self.detail_url = reverse('project-detail', kwargs={'pk': self.project.pk})

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    # TA02.01 — Criação bem-sucedida
    def test_create_project_success(self):
        self.authenticate(self.owner)
        data = {
            "title": "Novo Projeto",
            "description": "Descrição do projeto",
            "looking_for": "Desenvolvedor Python",
            "category": "startup"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Novo Projeto")
        self.assertEqual(response.data['status'], ProjectStatus.OPEN)

    # TA02.02 — Criação sem campos obrigatórios
    def test_create_project_missing_fields(self):
        self.authenticate(self.owner)
        data = {
            "title": "",
            "description": "",
            "looking_for": "Alguém",
            "category": "startup"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('description', response.data)

    # TA02.03 — Projeto aparece no feed da mesma instituição
    def test_feed_shows_own_institution_projects(self):
        self.authenticate(self.other_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Linkhub Frontend")

    # TA02.04 — Projeto não aparece para outra instituição
    def test_feed_hides_other_institution_projects(self):
        self.authenticate(self.ufpb_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # TA02.05 — Criador edita o projeto
    def test_owner_can_update_project(self):
        self.authenticate(self.owner)
        data = {
            "title": "Linkhub Atualizado",
            "description": "Nova descrição",
            "looking_for": "Novo perfil",
            "category": "open_source",
            "status": "in_progress"
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Linkhub Atualizado")
        self.assertEqual(response.data['status'], "in_progress")

    # TA02.06 — Não criador tenta editar
    def test_non_owner_cannot_update_project(self):
        self.authenticate(self.other_user)
        data = {
            "title": "Tentativa",
            "description": "Não deve funcionar",
            "looking_for": "Ninguém",
            "category": "other",
            "status": "open"
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # TA02.07 — Encerramento do projeto
    def test_owner_can_close_project(self):
        self.authenticate(self.owner)
        response = self.client.patch(
            self.detail_url,
            {"status": "completed"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "completed")

    # TA02.08 — Busca por título
    def test_search_by_title(self):
        self.authenticate(self.owner)
        response = self.client.get(self.list_url, {'search': 'Linkhub'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Linkhub', response.data[0]['title'])