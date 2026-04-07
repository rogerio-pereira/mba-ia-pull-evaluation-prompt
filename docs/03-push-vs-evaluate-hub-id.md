# Por que o `evaluate.py` dava 404 após o “push”?

## O que aconteceu

1. **`src/push_prompts.py` estava só com stubs (`...`)**  
   Rodar `python src/push_prompts.py` terminava sem erro, mas **não chamava a API do LangSmith**. Nada era publicado.

2. **Nome incompleto no hub**  
   No LangSmith, o prompt é sempre **`donodoPrompt/nomeDoRepo`**, por exemplo `meuusuario/bug_to_user_story_v2`.  
   O `evaluate.py` antigo chamava `hub.pull("bug_to_user_story_v2")`, e a API tentava algo como `.../commits/-/bug_to_user_story_v2/latest` — o `-` indica dono ausente — e respondia **404**.

## O que foi corrigido no código

- **`push_prompts.py`**: lê `prompts/bug_to_user_story_v2.yml`, valida e faz `hub.push` **público** em `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2`.
- **`evaluate.py`**: puxa `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2` (ou `EVAL_PROMPT_HUB_ID` no `.env`, se você quiser outro caminho).

## Checklist rápido

1. `.env` com `LANGSMITH_API_KEY` e **`USERNAME_LANGSMITH_HUB`** igual ao seu usuário no hub (prefixo antes da `/` no nome do prompt).
2. `prompts/bug_to_user_story_v2.yml` com a chave raiz **`bug_to_user_story_v2`** (não `bug_to_user_story_v1`).
3. `python src/push_prompts.py` e conferir no [dashboard de prompts](https://smith.langchain.com/prompts) se `seu_usuario/bug_to_user_story_v2` existe e está **público**.
4. `python src/evaluate.py`.

## Erro 409: “Nothing to commit”

Significa que o **conteúdo serializado do prompt** (mensagens system/human) é **igual** ao que já está no último commit do hub. Não é um bug: basta **alterar** `prompts/bug_to_user_story_v2.yml` e rodar o push de novo.

O `push_prompts.py` trata esse caso como **sucesso** (`✓ Nada a enviar`) para não bloquear o fluxo quando você só reenvia o mesmo arquivo.

## Variável opcional

- **`EVAL_PROMPT_HUB_ID`**: se quiser avaliar outro prompt do hub, defina o nome completo, ex.: `EVAL_PROMPT_HUB_ID=outrousuario/outro_prompt`.
