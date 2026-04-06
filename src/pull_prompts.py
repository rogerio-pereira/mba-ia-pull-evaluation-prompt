"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts.chat import (
    ChatMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

# ID no hub (owner/repo). Pode sobrescrever com variável de ambiente se necessário.
DEFAULT_HUB_PROMPT_ID = "leonanluppi/bug_to_user_story_v1"
ENV_HUB_PROMPT_ID = "PULL_PROMPT_HUB_ID"


def _template_text(message_template) -> str:
    """
    Lê o texto do template (string com variáveis tipo {bug_report}) de uma
    mensagem do ChatPromptTemplate.
    """
    inner = getattr(message_template, "prompt", None)
    if inner is None:
        return ""
    if hasattr(inner, "template"):
        return str(inner.template)
    return str(inner)


def _split_system_and_user_messages(
    chat_prompt: ChatPromptTemplate,
) -> tuple[str, str]:
    """
    Percorre as mensagens do prompt e separa texto de system e de user/human.
    Ordem: concatena várias system ou várias human com linha em branco entre elas.
    """
    system_parts: List[str] = []
    user_parts: List[str] = []

    for msg in chat_prompt.messages:
        if isinstance(msg, MessagesPlaceholder):
            # Placeholder de histórico (ex.: mensagens anteriores) — não vira YAML estático.
            continue

        text = _template_text(msg)
        if text.strip() == "":
            continue

        if isinstance(msg, SystemMessagePromptTemplate):
            system_parts.append(text)
            continue

        if isinstance(msg, HumanMessagePromptTemplate):
            user_parts.append(text)
            continue

        if isinstance(msg, ChatMessagePromptTemplate):
            role = (getattr(msg, "role", None) or "").lower()
            if role == "system":
                system_parts.append(text)
            else:
                # "human", "user", ou outros papéis viram lado "user" neste projeto.
                user_parts.append(text)
            continue

        # Tipo não previsto: mantém o texto para não perder conteúdo.
        user_parts.append(text)

    system_prompt = "\n\n".join(system_parts).strip()
    if len(user_parts) == 0:
        user_prompt = ""
    elif len(user_parts) == 1:
        user_prompt = user_parts[0].strip()
    else:
        user_prompt = "\n\n".join(user_parts).strip()

    return system_prompt, user_prompt


def _default_description(hub_prompt_id: str) -> str:
    return (
        "Prompt para converter relatos de bugs em User Stories "
        f"(fonte hub: {hub_prompt_id})"
    )


def chat_prompt_to_local_record(
    chat_prompt: ChatPromptTemplate,
    hub_prompt_id: str,
) -> Dict[str, Any]:
    """
    Monta o dicionário no formato do arquivo prompts/bug_to_user_story_v1.yml.
    """
    system_prompt, user_prompt = _split_system_and_user_messages(chat_prompt)

    if system_prompt == "":
        raise ValueError(
            "O prompt puxado não tinha mensagem de system. "
            "Confira o prompt no LangSmith Hub."
        )

    if user_prompt == "":
        # Dataset usa inputs['bug_report']; fallback seguro.
        variables = getattr(chat_prompt, "input_variables", None) or []
        if "bug_report" in variables:
            user_prompt = "{bug_report}"
        else:
            raise ValueError(
                "Não foi possível montar user_prompt e não há {bug_report} nas variáveis."
            )

    tags = ["bug-analysis", "user-story", "product-management"]
    metadata = getattr(chat_prompt, "metadata", None) or {}
    owner = metadata.get("lc_hub_owner")
    repo = metadata.get("lc_hub_repo")
    if owner and repo:
        tags = list(dict.fromkeys(tags + [f"hub:{owner}/{repo}"]))

    record: Dict[str, Any] = {
        "description": _default_description(hub_prompt_id),
        "system_prompt": system_prompt + "\n",
        "user_prompt": user_prompt,
        "version": "v1",
        "created_at": date.today().isoformat(),
        "tags": tags,
    }

    commit_hash = metadata.get("lc_hub_commit_hash")
    if commit_hash:
        record["hub_commit_hash"] = commit_hash

    return record


def pull_prompts_from_langsmith() -> Dict[str, Any]:
    hub_prompt_id = os.getenv(ENV_HUB_PROMPT_ID, DEFAULT_HUB_PROMPT_ID)

    print(f"Puxando prompt do hub: {hub_prompt_id}")
    pulled = hub.pull(hub_prompt_id)

    if not isinstance(pulled, ChatPromptTemplate):
        raise TypeError(
            "Esperado ChatPromptTemplate após hub.pull; recebido: "
            + type(pulled).__name__
        )

    return chat_prompt_to_local_record(pulled, hub_prompt_id)


def main() -> int:
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    project_root = Path(__file__).resolve().parent.parent
    output_path = project_root / "prompts" / "bug_to_user_story_v1.yml"

    try:
        record = pull_prompts_from_langsmith()
    except Exception as err:
        print(f"❌ Erro ao puxar prompt: {err}")
        return 1

    yaml_root: Dict[str, Any] = {"bug_to_user_story_v1": record}

    if not save_yaml(yaml_root, str(output_path)):
        return 1

    print(f"✓ Arquivo gravado em: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
