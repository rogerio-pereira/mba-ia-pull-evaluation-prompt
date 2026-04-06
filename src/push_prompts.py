"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()

YAML_RELATIVE = Path("prompts") / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"
HUB_REPO_NAME = "bug_to_user_story_v2"
ENV_USERNAME = "USERNAME_LANGSMITH_HUB"


def _push_is_unchanged_conflict(err: Exception) -> bool:
    """
    LangSmith responde 409 quando o manifest do prompt é idêntico ao último commit:
    "Nothing to commit: prompt has not changed since latest commit".
    """
    text = str(err).lower()
    if "409" not in text and "conflict" not in text:
        return False
    return "nothing to commit" in text or "has not changed" in text


def yaml_record_to_chat_template(prompt_data: dict) -> ChatPromptTemplate:
    """
    Monta um ChatPromptTemplate a partir dos campos system_prompt e user_prompt
    (placeholders como {bug_report} são mantidos).
    """
    system_text = (prompt_data.get("system_prompt") or "").strip()
    user_text = (prompt_data.get("user_prompt") or "").strip()
    if user_text == "":
        user_text = "{bug_report}"

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_text),
            ("human", user_text),
        ]
    )


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura do prompt antes do push (mesmas regras do utils + user_prompt).
    """
    is_valid, errors = validate_prompt_structure(prompt_data)
    errors = list(errors)

    user_prompt = (prompt_data.get("user_prompt") or "").strip()
    if user_prompt == "":
        errors.append("user_prompt está vazio (ou omitido)")

    return (len(errors) == 0, errors)


def push_prompt_to_langsmith(hub_repo_full_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        hub_repo_full_name: Nome completo owner/repo, ex.: joao/bug_to_user_story_v2
        prompt_data: Dados do prompt vindos do YAML

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        template = yaml_record_to_chat_template(prompt_data)
        api_key = os.getenv("LANGSMITH_API_KEY")

        tags = prompt_data.get("tags")
        if tags is not None:
            tags = list(tags)

        url = hub.push(
            hub_repo_full_name,
            template,
            api_key=api_key,
            new_repo_is_public=True,
            new_repo_description=prompt_data.get("description"),
            tags=tags,
        )
        print(f"✓ Push concluído. Ver no hub: {url}")
        return True

    except Exception as err:
        if _push_is_unchanged_conflict(err):
            print(
                "✓ Nada a enviar: o YAML local gera o mesmo prompt que já está no hub "
                f"({hub_repo_full_name}).\n"
                "  Edite prompts/bug_to_user_story_v2.yml (system_prompt, user_prompt, etc.) "
                "e rode o push de novo para criar um novo commit."
            )
            return True
        print(f"❌ Erro ao fazer push: {err}")
        return False


def main() -> int:
    print_section_header("PUSH DE PROMPTS AO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", ENV_USERNAME]
    if not check_env_vars(required_vars):
        return 1

    username = (os.getenv(ENV_USERNAME) or "").strip().strip("/")
    if username == "":
        print(f"❌ {ENV_USERNAME} não pode estar vazio. Confira o .env e docs/02-username-langsmith-hub.md")
        return 1

    project_root = Path(__file__).resolve().parent.parent
    yaml_path = project_root / YAML_RELATIVE

    if not yaml_path.is_file():
        print(f"❌ Arquivo não encontrado: {yaml_path}")
        return 1

    data = load_yaml(str(yaml_path))
    if data is None:
        return 1

    if PROMPT_KEY not in data:
        if "bug_to_user_story_v1" in data:
            print(
                "⚠️  O arquivo bug_to_user_story_v2.yml ainda usa a chave "
                "'bug_to_user_story_v1'. Troque para 'bug_to_user_story_v2'."
            )
        print(f"❌ Chave YAML obrigatória ausente: '{PROMPT_KEY}'")
        return 1

    prompt_data = data[PROMPT_KEY]
    is_ok, errors = validate_prompt(prompt_data)
    if not is_ok:
        print("❌ Validação do prompt falhou:")
        for err in errors:
            print(f"   - {err}")
        return 1

    hub_repo_full_name = f"{username}/{HUB_REPO_NAME}"
    print(f"Publicando prompt público: {hub_repo_full_name}")
    print("(Se o nome do repo no hub estiver errado, ajuste USERNAME_LANGSMITH_HUB no .env)\n")

    if not push_prompt_to_langsmith(hub_repo_full_name, prompt_data):
        return 1

    print(f"\n✓ Avalie com o mesmo identificador no hub:")
    print(f"    {hub_repo_full_name}")
    print("  (evaluate.py usa USERNAME_LANGSMITH_HUB automaticamente.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
