from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import User
from institutions.models import Institution


class AuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.refresh_url = '/api/auth/token/refresh/'
        self.me_url = '/api/users/me/'
        self.password_reset_url = '/api/auth/password-reset/'

    # TA01.01 — Cadastro bem-sucedido
    def test_register_success(self):
        response = self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Ciência da Computação'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'guilherme@ufrn.br')

    # TA01.02 — Domínio não institucional retorna erro
    def test_register_blocked_domain(self):
        response = self.client.post(self.register_url, {
            'name': 'Teste',
            'email': 'teste@gmail.com',
            'password': 'Senha@1234',
            'course': 'Teste'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TA01.03 — E-mail duplicado retorna conflito
    def test_register_duplicate_email(self):
        self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        response = self.client.post(self.register_url, {
            'name': 'Guilherme 2',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # TA01.04 — Login com credenciais válidas retorna tokens JWT
    def test_login_success(self):
        self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        response = self.client.post(self.login_url, {
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # TA01.05 — Login com senha incorreta retorna erro
    def test_login_wrong_password(self):
        self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        response = self.client.post(self.login_url, {
            'email': 'guilherme@ufrn.br',
            'password': 'SenhaErrada'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TA01.06 — Edição de perfil salva corretamente
    def test_update_profile(self):
        self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        login = self.client.post(self.login_url, {
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234'
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
        )
        response = self.client.put(self.me_url, {
            'name': 'Guilherme Atualizado',
            'course': 'Engenharia',
            'bio': 'Minha bio',
            'avatar_url': '',
            'skills': ['Python', 'Django'],
            'is_available': True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Guilherme Atualizado')
        self.assertEqual(response.data['bio'], 'Minha bio')

    # TA01.07 — Recuperação de senha retorna 200
    def test_password_reset_request(self):
        self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        response = self.client.post(self.password_reset_url, {
            'email': 'guilherme@ufrn.br'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TA01.08 — Perfil público exibe apenas dados permitidos
    def test_public_profile_isolation(self):
        # Cria usuário da mesma instituição
        self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        # Cria outro usuário da mesma instituição
        self.client.post(self.register_url, {
            'name': 'Kaio',
            'email': 'kaio@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        # Faz login como Guilherme
        login = self.client.post(self.login_url, {
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234'
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
        )
        kaio = User.objects.get(email='kaio@ufrn.br')
        response = self.client.get(f'/api/users/{kaio.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Não deve expor o e-mail no perfil público
        self.assertNotIn('email', response.data)

        # Cria usuário de outra instituição
        self.client.post(self.register_url, {
            'name': 'Outro',
            'email': 'outro@outra.edu.br',
            'password': 'Senha@1234',
            'course': 'Outro curso'
        })
        outro = User.objects.get(email='outro@outra.edu.br')
        response = self.client.get(f'/api/users/{outro.id}/')
        # Usuário de outra instituição retorna 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # TA01.07b — Confirmação de reset de senha com token válido
    def test_password_reset_confirm_success(self):
        # Cria usuário
        self.client.post(self.register_url, {
            'name': 'Guilherme',
            'email': 'guilherme@ufrn.br',
            'password': 'Senha@1234',
            'course': 'Computação'
        })
        user = User.objects.get(email='guilherme@ufrn.br')

        # Gera uid e token manualmente
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Confirma reset com nova senha
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'uid': uid,
            'token': token,
            'new_password': 'NovaSenha@5678'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Confirma que consegue logar com a nova senha
        login = self.client.post(self.login_url, {
            'email': 'guilherme@ufrn.br',
            'password': 'NovaSenha@5678'
        })
        self.assertEqual(login.status_code, status.HTTP_200_OK)

    # TA01.07c — Confirmação com token inválido retorna erro
    def test_password_reset_confirm_invalid_token(self):
        response = self.client.post('/api/auth/password-reset/confirm/', {
            'uid': 'uid-invalido',
            'token': 'token-invalido',
            'new_password': 'NovaSenha@5678'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)