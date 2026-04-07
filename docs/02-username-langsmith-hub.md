# `USERNAME_LANGSMITH_HUB` — quando precisa estar certo?

## Pull (baixar prompt de outra pessoa)

Para rodar `python src/pull_prompts.py` e puxar um prompt **já publicado** (ex.: `leonanluppi/bug_to_user_story_v1`), o que o LangSmith costuma exigir é uma **`LANGSMITH_API_KEY` válida** no `.env`.

Nesse fluxo, **`USERNAME_LANGSMITH_HUB` não é usado** pelo script de pull. Ou seja: pode estar vazio ou errado e o pull ainda assim funciona, desde que a API key e o nome do prompt no hub estejam corretos.

## Push (publicar o *seu* prompt)

Quando você for enviar o `bug_to_user_story_v2` com `python src/push_prompts.py`, aí sim o “dono” do prompt no hub é **o seu usuário**. O valor de `USERNAME_LANGSMITH_HUB` deve ser o **mesmo identificador de usuário/organização** que aparece nos prompts que você publica (o prefixo antes da barra, tipo `seu_nome/meu_prompt`).

### Como conferir o valor

1. Acesse o [LangSmith](https://smith.langchain.com/) e vá em **Prompts** (hub).
2. Abra um prompt **que você** publicou (ou o que o desafio pedir para criar).
3. O caminho costuma aparecer como `usuario/prompt_name`; use exatamente o `usuario` no `USERNAME_LANGSMITH_HUB`.

Dica do `.env.example`: às vezes o UI mostra um ícone de cadeado nas configurações de visibilidade do prompt — útil para confirmar o namespace.

## Resumo

| Etapa | Precisa de `USERNAME_LANGSMITH_HUB`? |
|--------|--------------------------------------|
| Pull do `leonanluppi/...` | Não |
| Push do seu `v2` | Sim (deve bater com seu usuário no hub) |
