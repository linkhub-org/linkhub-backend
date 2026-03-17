# Linkhub — Documento de Arquitetura

## 1. Visão Arquitetural

O Linkhub adota uma arquitetura de três camadas simples e linear: uma SPA em React no frontend, uma API REST em Django no backend e um banco de dados PostgreSQL. Não há serviços externos de fila ou cache no MVP — toda a lógica roda de forma síncrona.

```
┌─────────────────────────────────────────────────────┐
│                     FRONTEND                        │
│        React SPA  (Vite + React Router +            │
│              Axios + Tailwind CSS)                  │
└──────────────────────┬──────────────────────────────┘
                       │  HTTP / REST (JSON) + JWT
┌──────────────────────▼──────────────────────────────┐
│                     BACKEND                         │
│          Python  |  Django REST Framework           │
│                  |  SimpleJWT                       │
│                                                     │
│  users | institutions | projects | applications     │
│              notifications | feed                   │
└──────────────────────┬──────────────────────────────┘
                       │  Django ORM
┌──────────────────────▼──────────────────────────────┐
│                 BANCO DE DADOS                      │
│                   PostgreSQL                        │
└─────────────────────────────────────────────────────┘
```

---

## 2. Backend — Django REST Framework

### 2.1 Apps e Responsabilidades

| App | Responsabilidade |
|-----|-----------------|
| `core` | Settings, URLs globais, middlewares, utilitários |
| `users` | Cadastro, login, perfil e habilidades |
| `institutions` | Validação de domínio de e-mail e vínculo com usuário |
| `projects` | CRUD de projetos, categorias e status |
| `applications` | Candidaturas: criação, listagem, aceite e recusa |
| `notifications` | Geração síncrona e leitura de notificações |
| `feed` | Listagem cronológica com filtros por instituição |

### 2.2 Estrutura de Diretórios

```
linkhub-backend/
├── manage.py
├── requirements.txt
├── core/            # settings.py, urls.py, wsgi.py
├── users/           # models, serializers, views, urls, tests/
├── institutions/
├── projects/
├── applications/
├── notifications/
└── feed/
```

### 2.3 Autenticação — JWT

- **Biblioteca:** `djangorestframework-simplejwt`
- **Access token:** validade de 30 minutos
- **Refresh token:** validade de 7 dias
- Frontend envia o token no header: `Authorization: Bearer <token>`
- Endpoints protegidos validam o token a cada requisição via middleware

### 2.4 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/register/` | Cadastro com e-mail institucional |
| POST | `/api/auth/login/` | Login — retorna access e refresh token |
| POST | `/api/auth/token/refresh/` | Renovação do access token |
| GET / PUT | `/api/users/me/` | Perfil do usuário autenticado |
| GET | `/api/users/{id}/` | Perfil público de outro usuário |
| GET / POST | `/api/projects/` | Feed de projetos ou criação de novo projeto |
| GET / PUT / DELETE | `/api/projects/{id}/` | Detalhe, edição ou remoção de projeto |
| POST | `/api/projects/{id}/apply/` | Candidatar-se a um projeto |
| GET | `/api/projects/{id}/applications/` | Candidaturas do projeto (somente criador) |
| PATCH | `/api/applications/{id}/` | Aceitar ou recusar candidatura |
| GET / PATCH | `/api/notifications/` | Listar e marcar notificações como lidas |

---

## 3. Frontend — React

### 3.1 Estrutura de Diretórios

```
linkhub-frontend/
├── src/
│   ├── components/   # Componentes reutilizáveis
│   ├── pages/        # Feed, Projeto, Perfil, Login, Cadastro, CriarProjeto
│   ├── services/     # Funções Axios por domínio (auth, projects, applications...)
│   ├── context/      # AuthContext — usuário logado e token
│   ├── hooks/        # Custom hooks
│   ├── routes/       # React Router — rotas públicas e protegidas
│   └── utils/        # Helpers gerais
├── .env              # VITE_API_URL=https://...
└── package.json
```

### 3.2 Bibliotecas Principais

| Biblioteca | Finalidade |
|------------|------------|
| React Router DOM | Navegação entre páginas |
| Axios | Chamadas HTTP à API |
| Context API | Estado global de autenticação (usuário + token) |
| React Query | Cache e sincronização de dados do servidor |
| React Hook Form | Formulários com validação |
| Tailwind CSS | Estilização responsiva |

---

## 4. Banco de Dados — PostgreSQL

### 4.1 Entidades Principais

| Entidade | Atributos Principais | Relacionamentos |
|----------|---------------------|-----------------|
| `User` | id, name, email, password_hash, course, bio, avatar, skills, is_available | Pertence a 1 Institution; cria N Projects; faz N Applications |
| `Institution` | id, name, email_domain | Tem N Users e N Projects |
| `Project` | id, title, description, looking_for, category, status, created_at | Criado por 1 User; tem N Applications; pertence a 1 Institution |
| `Application` | id, message, status (pending/accepted/rejected), created_at | Feita por 1 User para 1 Project |
| `Notification` | id, type, message, is_read, created_at | Pertence a 1 User |

### 4.2 Decisões de Design

- O campo `looking_for` em `Project` substitui a entidade `Vacancy` — texto livre descrevendo o perfil buscado
- Skills do usuário são armazenadas como array de strings (`ArrayField` do PostgreSQL) ou tabela simples
- `Institution` é criada automaticamente ao detectar um novo domínio de e-mail no cadastro
- Todas as queries de projetos e usuários são filtradas por `institution_id`, garantindo isolamento entre instituições

---

## 5. Notificações — Fluxo Síncrono

Diferente de sistemas com filas assíncronas, as notificações no Linkhub são geradas de forma síncrona dentro da mesma transação da ação que as origina.

| Evento | Quem é notificado | Tipo |
|--------|------------------|------|
| Candidatura recebida | Criador do projeto | `new_application` |
| Candidatura aceita | Candidato | `application_accepted` |
| Candidatura recusada | Candidato | `application_rejected` |

O frontend consulta as notificações via polling leve (a cada 30s) ou ao carregar a página. Não há WebSocket no MVP.

---

## 6. Deployment Recomendado

**Recomendação para o MVP:** Railway (backend + banco) + Vercel (frontend).

| Serviço | O que hospeda | Custo |
|---------|--------------|-------|
| Railway | Backend Django + PostgreSQL | Plano gratuito para projetos acadêmicos |
| Vercel | Frontend React (build estático) | Gratuito sem limite de banda |
| Cloudinary *(opcional)* | Upload de fotos de perfil e projetos | Gratuito até 25GB |

### Variáveis de ambiente necessárias

- **Backend:** `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`
- **Frontend:** `VITE_API_URL` (URL do backend em produção)

---

## 7. Fluxo Completo de uma Requisição

**Exemplo: Estudante se candidata a um projeto.**

| Etapa | O que acontece |
|-------|---------------|
| 1. Clique em "Quero participar" | React chama `applications.create()` em `services/applications.js` |
| 2. Axios envia `POST /api/projects/{id}/apply/` | Header `Authorization: Bearer <token>` é incluído |
| 3. JWT Middleware valida o token | Usuário autenticado é injetado na requisição |
| 4. View valida as regras de negócio | Verifica: projeto aberto, usuário não é criador, não candidatou antes |
| 5. Application criada no banco | Status: `PENDING` |
| 6. Notificação criada no mesmo request | Registro inserido na tabela `Notification` para o criador do projeto |
| 7. API retorna `201 Created` | JSON com os dados da candidatura |
| 8. React Query invalida o cache | Botão muda para "Candidatura enviada" |