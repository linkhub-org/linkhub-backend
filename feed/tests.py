from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from users.models import User
from projects.models import Project


def create_user(email, name="Usuário"):
    return User.objects.create_user(
        email=email,
        name=name,
        password="Senha@1234",
        course="Computação"
    )

def create_project(owner, title="Projeto", category="academic", status="open"):
    return Project.objects.create(
        title=title,
        description="Descrição",
        looking_for="Desenvolvedor",
        category=category,
        status=status,
        owner=owner,
        institution=owner.institution
    )

def login(client, email):
    response = client.post('/api/auth/login/', {
        'email': email,
        'password': 'Senha@1234'
    })
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")


class FeedTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user('guilherme@ufrn.br', 'Guilherme')
        login(self.client, 'guilherme@ufrn.br')

    # TA04.01 — Feed exibe apenas projetos da mesma instituição
    def test_feed_shows_only_same_institution(self):
        create_project(self.user, title="Projeto UFRN")
        other_user = create_user('outro@ufpb.br', 'Outro')
        create_project(other_user, title="Projeto UFPB")
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [p['title'] for p in response.data]
        self.assertIn("Projeto UFRN", titles)
        self.assertNotIn("Projeto UFPB", titles)

    # TA04.02 — Feed ordenado do mais recente para o mais antigo
    def test_feed_ordered_by_created_at(self):
        create_project(self.user, title="Projeto A")
        create_project(self.user, title="Projeto B")
        create_project(self.user, title="Projeto C")
        response = self.client.get('/api/feed/')
        dates = [p['created_at'] for p in response.data]
        self.assertEqual(dates, sorted(dates, reverse=True))

    # TA04.03 — Filtro por categoria
    def test_feed_filter_by_category(self):
        create_project(self.user, title="Startup X", category="startup")
        create_project(self.user, title="Acadêmico Y", category="academic")
        response = self.client.get('/api/feed/?category=startup')
        titles = [p['title'] for p in response.data]
        self.assertIn("Startup X", titles)
        self.assertNotIn("Acadêmico Y", titles)

    # TA04.04 — Filtro por status
    def test_feed_filter_by_status(self):
        create_project(self.user, title="Aberto", status="open")
        create_project(self.user, title="Concluído", status="completed")
        response = self.client.get('/api/feed/?status=open')
        titles = [p['title'] for p in response.data]
        self.assertIn("Aberto", titles)
        self.assertNotIn("Concluído", titles)

    # TA04.05 — Filtros combinados
    def test_feed_filter_combined(self):
        create_project(self.user, title="Startup Aberto", category="startup", status="open")
        create_project(self.user, title="Startup Concluído", category="startup", status="completed")
        create_project(self.user, title="Acadêmico Aberto", category="academic", status="open")
        response = self.client.get('/api/feed/?category=startup&status=open')
        titles = [p['title'] for p in response.data]
        self.assertIn("Startup Aberto", titles)
        self.assertNotIn("Startup Concluído", titles)
        self.assertNotIn("Acadêmico Aberto", titles)

    # TA04.06 — Busca por título
    def test_feed_search_by_title(self):
        create_project(self.user, title="Robótica Avançada")
        create_project(self.user, title="Machine Learning")
        response = self.client.get('/api/feed/?search=Robótica')
        titles = [p['title'] for p in response.data]
        self.assertIn("Robótica Avançada", titles)
        self.assertNotIn("Machine Learning", titles)

    # TA04.07 — Busca sem resultados retorna lista vazia
    def test_feed_search_no_results(self):
        response = self.client.get('/api/feed/?search=xyzabc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)