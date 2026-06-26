import json
from groq import Groq
from decouple import config
from rest_framework.exceptions import APIException


class AIUnavailableException(APIException):
    status_code = 503
    default_detail = "Serviço de IA temporariamente indisponível."
    default_code = "ai_unavailable"


def _get_client():
    return Groq(api_key=config('GROQ_API_KEY'))


def recommend_profiles_for_project(project, available_profiles):
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

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.3,
        )
        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        return json.loads(raw)
    except json.JSONDecodeError:
        raise AIUnavailableException(detail="Resposta da IA em formato inválido.")
    except Exception as e:
        raise AIUnavailableException(detail=f"Erro na API de IA: {str(e)}")


def recommend_projects_for_user(user, available_projects):
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

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.3,
        )
        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        return json.loads(raw)
    except json.JSONDecodeError:
        raise AIUnavailableException(detail="Resposta da IA em formato inválido.")
    except Exception as e:
        raise AIUnavailableException(detail=f"Erro na API de IA: {str(e)}")