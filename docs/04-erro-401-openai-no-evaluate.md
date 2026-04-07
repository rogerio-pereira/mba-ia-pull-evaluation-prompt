# Erro 401 no `evaluate.py` (OpenAI)

## Sintomas

- Mensagens como: `Error code: 401`, `invalid_api_key`, `Incorrect API key provided`.
- Todas as métricas aparecem **0.00** e o status **REPROVADO**, mesmo com o prompt carregando do hub.

## Causa

O script chama a API da **OpenAI** para gerar respostas (`LLM_MODEL`, ex.: `gpt-4o-mini`). O **401** significa que `OPENAI_API_KEY` no `.env` não é aceita pela OpenAI.

Chaves de **outros produtos** (por exemplo prefixos que não são o padrão `sk-...` da OpenAI) **não** funcionam na API `api.openai.com`.

## O que fazer

1. Gere uma chave em [API keys OpenAI](https://platform.openai.com/api-keys).
2. Defina no `.env`: `OPENAI_API_KEY=sk-...` (valor real da plataforma OpenAI).
3. Verifique `LLM_PROVIDER=openai` e modelos compatíveis com sua conta.

## Alternativa: Google Gemini

No `.env`: `LLM_PROVIDER=google`, `GOOGLE_API_KEY` com chave do [Google AI Studio](https://aistudio.google.com/app/apikey), e variáveis de modelo conforme o `README.md` do desafio.

## Lembrete

**LangSmith** (`LANGSMITH_API_KEY`) e **OpenAI** (`OPENAI_API_KEY`) são serviços diferentes: um pode estar certo e o outro errado. O pull do prompt no hub pode funcionar mesmo com a chave OpenAI inválida.
