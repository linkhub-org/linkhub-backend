# Linkhub — Diagrama de Classes (UML)

Documento feito a partir do [Documento de Visão](doc-visao.md) e do [Documento de Arquitetura](doc-arquitetura.md).

---

## Diagrama

```mermaid
classDiagram

    class Institution {
        +int id
        +String name
        +String email_domain
        +create_from_email(email: String) Institution$
        +find_by_domain(domain: String) Institution$
    }

    class User {
        +int id
        +String name
        +String email
        +String password_hash
        +String course
        +String bio
        +String avatarURL
        +List~String~ skills
        +bool is_available
        +Institution institution
        +register(name, email, password, course) User$
        +authenticate(email, password) TokenPair$
        +update_profile(data: dict) void
        +request_password_reset() void
        +get_public_profile() dict
    }

    class Project {
        +int id
        +String title
        +String description
        +String looking_for
        +String category
        +ProjectStatus status
        +datetime created_at
        +User owner
        +Institution institution
        +create(owner, data) Project$
        +update(data: dict) void
        +close(status: ProjectStatus) void
        +get_members() List~User~
        +is_open() bool
    }

    class ProjectStatus {
        <<enumeration>>
        OPEN
        IN_PROGRESS
        COMPLETED
        CANCELLED
    }

    class ProjectCategory {
        <<enumeration>>
        ACADEMIC
        STARTUP
        OPEN_SOURCE
        SOCIAL
        OTHER
    }

    class Application {
        +int id
        +String message
        +ApplicationStatus status
        +datetime created_at
        +User applicant
        +Project project
        +create(applicant, project, message) Application$
        +accept() void
        +reject() void
        +cancel() void
        +validate_unique() void
        +validate_not_owner() void
    }

    class ApplicationStatus {
        <<enumeration>>
        PENDING
        ACCEPTED
        REJECTED
    }

    class ProjectMember {
        +int id
        +Project project
        +User user
        +datetime joined_at
        +create_from_application(application) ProjectMember$
    }

    class Notification {
        +int id
        +NotificationType type
        +String message
        +bool is_read
        +datetime created_at
        +User recipient
        +create(recipient, type, message) Notification$
        +mark_as_read() void
    }

    class NotificationType {
        <<enumeration>>
        NEW_APPLICATION
        APPLICATION_ACCEPTED
        APPLICATION_REJECTED
    }

    class AuthService {
        <<service>>
        +login(email, password) TokenPair$
        +refresh_token(refresh_token) AccessToken$
        +validate_institutional_email(email) bool$
        +extract_domain(email) String$
    }

    class NotificationService {
        <<service>>
        +notify_new_application(application) void$
        +notify_application_result(application) void$
    }

    class FeedService {
        <<service>>
        +get_feed(user, filters) List~Project~$
        +search(user, query) List~Project~$
    }

    %% Relacionamentos de herança / composição
    User "N" --> "1" Institution : pertence a
    Project "N" --> "1" User : criado por
    Project "N" --> "1" Institution : pertence a
    Project --> ProjectStatus : tem
    Project --> ProjectCategory : tem

    Application "N" --> "1" User : feita por
    Application "N" --> "1" Project : para
    Application --> ApplicationStatus : tem

    ProjectMember "N" --> "1" Project : membro de
    ProjectMember "N" --> "1" User : é

    Notification "N" --> "1" User : destinatário
    Notification --> NotificationType : tem

    %% Dependências de serviços
    AuthService ..> User : usa
    AuthService ..> Institution : usa
    NotificationService ..> Notification : cria
    NotificationService ..> Application : observa
    FeedService ..> Project : consulta
    FeedService ..> Institution : filtra por

    %% Criação encadeada
    Application ..> ProjectMember : cria ao aceitar
    Application ..> NotificationService : aciona
```

---

## Descrição das Classes

### Entidades de Domínio

| Classe | Responsabilidade |
|--------|-----------------|
| `Institution` | Representa uma instituição de ensino. Criada automaticamente ao detectar um novo domínio de e-mail. |
| `User` | Estudante cadastrado na plataforma. Possui perfil, habilidades e disponibilidade. |
| `Project` | Iniciativa criada por um estudante. Visível apenas para usuários da mesma instituição. |
| `Application` | Candidatura de um estudante a um projeto. Contém validações de unicidade e propriedade. |
| `ProjectMember` | Criada automaticamente ao aceitar uma candidatura. Representa o vínculo entre estudante e projeto. |
| `Notification` | Aviso gerado de forma síncrona em resposta a eventos de candidatura. |

### Enumerações

| Enumeração | Valores |
|------------|---------|
| `ProjectStatus` | OPEN, IN_PROGRESS, COMPLETED, CANCELLED |
| `ProjectCategory` | ACADEMIC, STARTUP, OPEN_SOURCE, SOCIAL, OTHER |
| `ApplicationStatus` | PENDING, ACCEPTED, REJECTED |
| `NotificationType` | NEW_APPLICATION, APPLICATION_ACCEPTED, APPLICATION_REJECTED |

### Serviços

| Serviço | Responsabilidade |
|---------|-----------------|
| `AuthService` | Autenticação JWT, validação de domínio institucional e geração de tokens. |
| `NotificationService` | Geração síncrona de notificações em resposta a eventos de candidatura. |
| `FeedService` | Montagem do feed cronológico com filtros por instituição, categoria e status. |

---

## Rastreabilidade com os Requisitos

| Classe / Elemento | Requisitos Cobertos |
|-------------------|---------------------|
| `User` + `AuthService` | RF01.01, RF01.02, RF01.03, RF01.04, RF01.05, RF01.06 |
| `Project` + `FeedService` | RF02.01, RF02.02, RF02.03, RF02.04, RF02.05, RF02.06 |
| `Application` + `ProjectMember` | RF03.01, RF03.02, RF03.03, RF03.04, RF03.05 |
| `Notification` + `NotificationService` | RF04.01, RF04.02, RF04.03, RF04.04 |