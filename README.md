# Linkhub — Backend

> API REST do Linkhub — Rede social de projetos universitários.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Django](https://img.shields.io/badge/django-6.x-green)
![PostgreSQL](https://img.shields.io/badge/postgresql-14+-blue)

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado na sua máquina:

- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [PostgreSQL 14+](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)

---

## Configuração do Banco de Dados

**1.** Abra o pgAdmin e conecte com o usuário `postgres`.

**2.** Clique com botão direito em **Databases → Create → Database**.

**3.** Nome: `linkhub` → clique em **Save**.

---

## Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/linkhub-backend.git
cd linkhub-backend
```

### 2. Crie e ative o ambiente virtual

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Você saberá que funcionou quando o terminal mostrar `(venv)` no início da linha.

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (mesma pasta do `manage.py`):

```env
SECRET_KEY=django-insecure-mude-essa-chave-antes-de-ir-para-producao
DEBUG=True
DB_NAME=linkhub
DB_USER=postgres
DB_PASSWORD=sua-senha-do-postgres
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

> Substitua `sua-senha-do-postgres` pela senha definida na instalação do PostgreSQL.

### 5. Execute as migrations

```bash
python manage.py migrate
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://localhost:8000`

---

## Documentação da API

Com o servidor rodando, acesse:

```
http://localhost:8000/api/docs/
```

Você verá a interface do Swagger com todos os endpoints disponíveis.

---

## Endpoints Implementados (Sprint 1)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/auth/register/` | Cadastro com e-mail institucional | ✗ |
| POST | `/api/auth/login/` | Login — retorna tokens JWT | ✗ |
| POST | `/api/auth/token/refresh/` | Renovação do access token | ✗ |
| POST | `/api/auth/password-reset/` | Solicitação de recuperação de senha | ✗ |
| GET / PUT | `/api/users/me/` | Perfil do usuário autenticado | ✓ |
| GET | `/api/users/{id}/` | Perfil público de outro usuário | ✓ |

---

## Como autenticar no Swagger

**1.** Faça login em `POST /api/auth/login/` com suas credenciais e copie o valor do campo `access`.

**2.** Clique no botão **Authorize** (cadeado 🔒) no topo da página.

**3.** No campo que aparecer, digite:
```
SEU_TOKEN_AQUI
```

**4.** Clique em **Authorize** → **Close**. Agora você pode usar os endpoints protegidos.

---

## Estrutura do Projeto

```
linkhub-backend/
├── core/                  # Settings, URLs globais, wsgi
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── institutions/          # Model Institution
│   └── models.py
├── users/                 # Autenticação e perfil
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── password_reset.py
├── projects/              # (Sprint 2 — Kaio)
├── applications/          # (Sprint 3 — Kaio)
├── notifications/         # (Sprint 4 — Guilherme)
├── feed/                  # (Sprint 4 — Guilherme)
├── docs/                  # Documentação do projeto
├── manage.py
├── requirements.txt
├── .env                   # NÃO versionar — criar localmente
└── .gitignore
```

---

## Convenções do Projeto

### Branches

| Branch | Uso |
|--------|-----|
| `main` | Código estável, revisado |
| `dev` | Branch de integração |
| `feat/nome-da-feature` | Nova funcionalidade |
| `fix/nome-do-bug` | Correção de bug |

### Commits

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/) em inglês:

```
feat: add application endpoint
fix: fix institutional domain validation
docs: update README
test: add users module tests
refactor: reorganize user serializers
```

### Pull Requests

- Sempre abrir PR para a branch `dev`
- Aguardar revisão antes de fazer **squash and merge**
- Descrever o que foi feito e referenciar a tarefa do cronograma

---

## Equipe

| Membro | Papel |
|--------|-------|
| Guilherme | Gerente, Desenvolvedor (US01, US04, US05) |
| Kaio | Analista, Desenvolvedor (US02, US03) |

---

# Documentação
- [Diagrama de Classes](./docs/diagrama-classes.md)
- [Arquitetura](./docs/doc-arquitetura.md)
- [UserStories](./docs/doc-userstories.md)
- [Visão](./docs/doc-visao.md)
