# Linkhub — Documento de User Stories

## Descrição

Este documento descreve os User Stories criados a partir da Lista de Requisitos no [Documento de Visão](doc-visao.md). O Linkhub é uma rede social de projetos universitários cujo acesso é restrito por e-mail institucional, conectando estudantes da mesma instituição a projetos de interesse mútuo.

### User Story US01 — Manter Usuário

| | |
| --- | :--- |
| **Descrição** | O sistema deve manter um cadastro de usuário que tem acesso ao sistema via e-mail institucional e senha. Um usuário possui os atributos id, name, email, password, course, bio, avatarURL, skills e is_available. O e-mail deve pertencer ao domínio da instituição de ensino e é usado como login. O vínculo com a instituição é feito automaticamente pelo domínio do e-mail no cadastro. O avatarURL é um link para a foto de perfil do estudante. O próprio usuário pode editar seus dados após o cadastro. |

| **Requisitos Envolvidos** | |
| --- | :--- |
| RF01.01 | Cadastrar Usuário com e-mail institucional |
| RF01.02 | Login com e-mail e senha |
| RF01.03 | Recuperar Senha por e-mail |
| RF01.04 | Visualizar Perfil Próprio | 
| RF01.05 | Atualizar Perfil (name, bio, avatarURL, course, skills, is_available) |
| RF01.06 | Visualizar Perfil Público de outro usuário da mesma instituição |

| | |
| --- | --- |
| **Prioridade** | Essencial |
| **Estimativa** | 10h |
| **Tempo Gasto (real)** | |
| **Tamanho Funcional** | 8 PF |
| **Analista** | Kaio |
| **Desenvolvedor** | Guilherme |
| **Revisor** | Kaio |
| **Testador** | Guilherme |

| Testes de Aceitação (TA) | |
| --- | :--- |
| **Código** | **Descrição** |
| **TA01.01** | Cadastro bem-sucedido com e-mail institucional válido e todos os campos obrigatórios preenchidos. |
| **TA01.02** | Tentativa de cadastro com e-mail de domínio não institucional retorna mensagem de erro. |
| **TA01.03** | Tentativa de cadastro com e-mail já existente retorna mensagem de conflito. |
| **TA01.04** | Login bem-sucedido com credenciais válidas retorna token JWT de acesso e refresh. |
| **TA01.05** | Login com senha incorreta retorna erro de autenticação. |
| **TA01.06** | Edição de perfil salva corretamente e os dados atualizados são refletidos na interface. |
| **TA01.07** | Solicitação de recuperação de senha com e-mail válido dispara o envio do e-mail de recuperação. |
| **TA01.08** | Visualização do perfil público exibe apenas os dados permitidos de um usuário da mesma instituição. |

---

### User Story US02 — Manter Projeto

| | |
| --- | :--- |
| **Descrição** | O sistema deve manter um cadastro de projetos criados por usuários autenticados. Um projeto possui os atributos id, title, description, looking_for, category, status e created_at. O campo looking_for descreve em texto livre o perfil buscado. As categorias possíveis são: Acadêmico, Startup, Open Source, Social e Outros. O status pode ser: Aberto, Em andamento, Concluído ou Cancelado. Apenas o criador pode editar ou encerrar o projeto. |

| **Requisitos Envolvidos** | |
| --- | :--- |
| RF02.01 | Inserir Projeto informando title, description, looking_for e category |
| RF02.02 | Listar Projetos (Feed) da mesma instituição em ordem cronológica, com filtros |
| RF02.03 | Buscar Projetos pelo título ou categoria |
| RF02.04 | Visualizar detalhes do Projeto com membros atuais |
| RF02.05 | Atualizar Projeto (restrito ao criador) |
| RF02.06 | Encerrar Projeto alterando status para Concluído ou Cancelado (restrito ao criador) |

| | |
| --- | --- |
| **Prioridade** | Essencial |
| **Estimativa** | 10h |
| **Tempo Gasto (real)** | |
| **Tamanho Funcional** | 7 PF |
| **Analista** | Guilherme |
| **Desenvolvedor** | Kaio |
| **Revisor** | Guilherme |
| **Testador** | Kaio |

| Testes de Aceitação (TA) | |
| --- | :--- |
| **Código** | **Descrição** |
| **TA02.01** | Criação bem-sucedida de projeto com todos os campos obrigatórios preenchidos. |
| **TA02.02** | Tentativa de criação de projeto sem título ou descrição retorna erro de validação. |
| **TA02.03** | Projeto criado aparece no feed para usuários da mesma instituição. |
| **TA02.04** | Projeto não aparece no feed de usuários de outras instituições. |
| **TA02.05** | Criador consegue editar título, descrição, looking_for, category e status do projeto. |
| **TA02.06** | Usuário não criador tenta editar o projeto e recebe erro 403 (Forbidden). |
| **TA02.07** | Encerramento do projeto altera o status corretamente e impede novas candidaturas. |
| **TA02.08** | Busca por título retorna projetos cujo nome contenha o termo digitado. |

---

### User Story US03 — Manter Candidatura

| | |
| --- | :--- |
| **Descrição** | O sistema deve manter o registro de candidaturas de estudantes a projetos. Uma candidatura possui os atributos id, message, status e created_at. Os status possíveis são: pending, accepted e rejected. O usuário não pode candidatar-se ao próprio projeto nem enviar mais de uma candidatura ao mesmo projeto. Quando aceita, a candidatura gera um registro em ProjectMember, adicionando o candidato como membro. O candidato pode cancelar sua candidatura enquanto o status for pending. |

| **Requisitos Envolvidos** | |
| --- | :--- |
| RF03.01 | Inserir Candidatura com mensagem de apresentação |
| RF03.02 | Listar Candidaturas recebidas por projeto (restrito ao criador) |
| RF03.03 | Aceitar Candidatura e adicionar candidato como membro via ProjectMember |
| RF03.04 | Recusar Candidatura |
| RF03.05 | Cancelar Candidatura pelo candidato enquanto pendente |

| | |
| --- | --- |
| **Prioridade** | Essencial |
| **Estimativa** | 8h |
| **Tempo Gasto (real)** | |
| **Tamanho Funcional** | 6 PF |
| **Analista** | Guilherme |
| **Desenvolvedor** | Kaio |
| **Revisor** | Guilherme |
| **Testador** | Kaio |

| Testes de Aceitação (TA) | |
| --- | :--- |
| **Código** | **Descrição** |
| **TA03.01** | Candidatura bem-sucedida com mensagem preenchida retorna status HTTP 201. |
| **TA03.02** | Tentativa de candidatura sem mensagem de apresentação retorna erro de validação. |
| **TA03.03** | Segunda candidatura ao mesmo projeto retorna erro de conflito. |
| **TA03.04** | Criador do projeto tenta se candidatar ao próprio projeto e recebe erro 403 (Forbidden). |
| **TA03.05** | Criador aceita candidatura: status muda para accepted e candidato é adicionado como membro via ProjectMember. |
| **TA03.06** | Criador recusa candidatura: status muda para rejected corretamente. |
| **TA03.07** | Candidato cancela candidatura com status pending com sucesso via DELETE /api/applications/{id}/. |
| **TA03.08** | Candidato tenta cancelar candidatura já aceita ou recusada e recebe erro de validação. |

---

### User Story US04 — Visualizar Feed de Projetos

| | |
| --- | :--- |
| **Descrição** | O sistema deve exibir ao usuário autenticado um feed cronológico com os projetos publicados na sua instituição. O feed deve suportar filtros independentes e combinados por categoria e status, além de permitir busca por nome. Somente projetos de usuários da mesma instituição devem ser exibidos. Quando nenhum projeto for encontrado, o sistema deve informar o usuário. |

| **Requisitos Envolvidos** | |
| --- | :--- |
| RF02.02 | Listar Projetos (Feed) cronológico da mesma instituição, com filtros por categoria e status |
| RF02.03 | Buscar Projetos por título ou categoria |

| | |
| --- | --- |
| **Prioridade** | Essencial |
| **Estimativa** | 6h |
| **Tempo Gasto (real)** | |
| **Tamanho Funcional** | 5 PF |
| **Analista** | Kaio |
| **Desenvolvedor** | Guilherme |
| **Revisor** | Kaio |
| **Testador** | Guilherme |

| Testes de Aceitação (TA) | |
| --- | :--- |
| **Código** | **Descrição** |
| **TA04.01** | Feed exibe apenas projetos de usuários da mesma instituição do usuário autenticado. |
| **TA04.02** | Projetos do feed estão ordenados do mais recente para o mais antigo. |
| **TA04.03** | Filtro por categoria "Startup" retorna somente projetos dessa categoria. |
| **TA04.04** | Filtro por status "Aberto" retorna somente projetos com esse status. |
| **TA04.05** | Filtros de categoria e status aplicados simultaneamente retornam resultado combinado correto. |
| **TA04.06** | Busca pelo título retorna projetos cujo nome contenha o termo digitado. |
| **TA04.07** | Busca sem resultados exibe a mensagem "Nenhum projeto encontrado". |

---

### User Story US05 — Manter Notificações

| | |
| --- | :--- |
| **Descrição** | O sistema deve gerar e exibir notificações para os usuários com base em eventos de candidatura. As notificações possuem os atributos id, type, message, is_read e created_at. Os tipos possíveis são: new_application (para o criador), application_accepted e application_rejected (para o candidato). As notificações são geradas de forma síncrona, na mesma transação do evento que as originou. O usuário pode marcar notificações como lidas individualmente. |

| **Requisitos Envolvidos** | |
| --- | :--- |
| RF04.01 | Gerar notificação ao criador quando candidatura for recebida |
| RF04.02 | Gerar notificação ao candidato quando candidatura for aceita ou recusada |
| RF04.03 | Listar Notificações em ordem cronológica decrescente |
| RF04.04 | Marcar Notificação como lida |

| | |
| --- | --- |
| **Prioridade** | Essencial |
| **Estimativa** | 5h |
| **Tempo Gasto (real)** | |
| **Tamanho Funcional** | 4 PF |
| **Analista** | Kaio |
| **Desenvolvedor** | Guilherme |
| **Revisor** | Kaio |
| **Testador** | Guilherme |

| Testes de Aceitação (TA) | |
| --- | :--- |
| **Código** | **Descrição** |
| **TA05.01** | Ao receber uma candidatura, o criador visualiza notificação do tipo new_application. |
| **TA05.02** | Ao ter candidatura aceita, o candidato visualiza notificação do tipo application_accepted. |
| **TA05.03** | Ao ter candidatura recusada, o candidato visualiza notificação do tipo application_rejected. |
| **TA05.04** | Notificações não lidas são exibidas com destaque visual distinto das já lidas. |
| **TA05.05** | Ao marcar notificação como lida, o destaque visual é removido e is_read é atualizado no banco. |
| **TA05.06** | Notificações são listadas da mais recente para a mais antiga. |