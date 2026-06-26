import json
import anthropic
from decouple import config


def _get_client():
    return anthropic.Anthropic(api_key=config('ANTHROPIC_API_KEY'))


def recommend_profiles_for_project(project, available_profiles):
    """
    Recebe um Project e uma lista/queryset de Users disponíveis.
    Retorna lista de dicts: [{user_id, name, reason}, ...]
    """
    if not available_profiles:
        return []

    profiles_text = "\n".join([
        f"- ID {p.id}: {p.name} | Curso: {p.course or 'Não informado'} | "
        f"Bio: {p.bio or 'Não informada'} | "
        f"Habilidades: {', '.join(p.skills) if p.skills else 'Não informadas'}"
        for p in available_profiles
    ])

    prompt = f"""Você é um assistente de recrutamento universitário.

Projeto:
- Título: {project.title}
- Descrição: {project.description}
- Perfil buscado: {project.looking_for}
- Categoria: {project.get_category_display()}

Perfis disponíveis na instituição (excluindo membros atuais):
{profiles_text}

Recomende os 3 perfis mais compatíveis com este projeto.
Para cada um, explique em 1-2 frases por que é uma boa escolha.

Responda APENAS em JSON válido, sem texto adicional, sem markdown, no formato:
[
  {{
    "user_id": 1,
    "name": "Nome",
    "reason": "Justificativa"
  }}
]"""

    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    return json.loads(raw)


def recommend_projects_for_user(user, available_projects):
    """
    Recebe um User e uma lista/queryset de Projects disponíveis.
    Retorna lista de dicts: [{project_id, title, reason}, ...]
    """
    if not available_projects:
        return []

    projects_text = "\n".join([
        f"- ID {p.id}: {p.title} | "
        f"Descrição: {p.description[:200]} | "
        f"Perfil buscado: {p.looking_for[:150]} | "
        f"Categoria: {p.get_category_display()}"
        for p in available_projects
    ])

    prompt = f"""Você é um assistente de conexão universitária.

Perfil do usuário:
- Nome: {user.name}
- Curso: {user.course or 'Não informado'}
- Bio: {user.bio or 'Não informada'}
- Habilidades: {', '.join(user.skills) if user.skills else 'Não informadas'}

Projetos disponíveis na instituição (excluindo projetos que já participa):
{projects_text}

Recomende os 3 projetos mais compatíveis com este perfil.
Para cada um, explique em 1-2 frases por que é uma boa escolha.

Responda APENAS em JSON válido, sem texto adicional, sem markdown, no formato:
[
  {{
    "project_id": 1,
    "title": "Título",
    "reason": "Justificativa"
  }}
]"""

    client = _get_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    return json.loads(raw)