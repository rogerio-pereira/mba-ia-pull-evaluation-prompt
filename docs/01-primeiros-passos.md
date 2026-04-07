# Primeiros passos do projeto (baby steps)

Este guia resume o que fazer **logo no início**, antes de otimizar prompts ou rodar avaliações completas. O desafio está descrito no `README.md` na raiz do repositório.

---

## Passo 0 — Entender o que você vai construir

Em ordem natural do trabalho:

1. **Pull**: baixar o prompt “ruim” do LangSmith para a máquina local.
2. **Otimizar**: criar/editar o YAML do prompt melhorado (`prompts/bug_to_user_story_v2.yml`).
3. **Push**: enviar o prompt otimizado de volta ao LangSmith (com seu usuário no hub).
4. **Avaliar**: rodar `evaluate.py` e iterar até todas as métricas ≥ 0.9.

Neste momento, foque só nos passos 0–2 da seção abaixo (ambiente + credenciais + primeiro pull).

---

## Passo 1 — Verificar Python

O projeto pede **Python 3.9+**.

```bash
python3 --version
```

Se a versão for menor que 3.9, instale ou use outra versão (por exemplo via `pyenv` ou pacote do sistema).

---

## Passo 2 — Ambiente virtual (equivalente ao “composer local” do PHP)

No PHP costuma-se isolar dependências por projeto; em Python isso é feito com **venv**.

Na raiz do repositório:

```bash
cd /caminho/para/Desafio02
python3 -m venv venv
source venv/bin/activate
```

No Windows (PowerShell): `venv\Scripts\Activate.ps1`

Enquanto o venv estiver ativado, o comando `pip` instala só neste projeto.

---

## Passo 3 — Instalar dependências

```bash
pip install -r requirements.txt
```

Se algo falhar, copie a mensagem de erro completa — costuma ser versão de Python ou falta de compilador para algum pacote.

---

## Passo 4 — Credenciais (arquivo `.env`)

1. Copie o exemplo:

   ```bash
   cp .env.example .env
   ```

2. Edite o `.env` e preencha pelo menos:
   - **LangSmith**: `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT` (e tracing/endpoint conforme o exemplo).
   - **Username no hub**: `USERNAME_LANGSMITH_HUB` (instrução no próprio `.env.example`).
   - **LLM**: escolha **OpenAI** ou **Google** e preencha `OPENAI_API_KEY` ou `GOOGLE_API_KEY`; ajuste `LLM_PROVIDER`, `LLM_MODEL` e `EVAL_MODEL` como no README do desafio.

**Dica:** nunca commite o `.env` — ele costuma estar no `.gitignore`. Só o `.env.example` vai para o Git.

---

## Passo 5 — Primeiro comando útil: pull dos prompts

Com o venv ativado e o `.env` configurado:

```bash
python src/pull_prompts.py
```

Objetivo (README do desafio): puxar o prompt `leonanluppi/bug_to_user_story_v1` e guardar localmente. No código-base, o comentário em `src/pull_prompts.py` indica saída em `prompts/bug_to_user_story_v1.yml` (o README do template às vezes menciona `raw_prompts.yml` — use o caminho que o seu script realmente gravar).

Se der erro de autenticação, revise `LANGSMITH_API_KEY` e variáveis de projeto no LangSmith.

---

## Passo 6 — Olhar o que foi baixado

Abra:

- `prompts/bug_to_user_story_v1.yml` (ou o arquivo que o pull gerar/atualizar)

Assim você vê o formato YAML (system/user messages, etc.) antes de criar a `v2`.

---

## Ordem sugerida depois disso (visão curta)

| Ordem | Ação |
|------|------|
| 1 | Completar/ajustar `pull_prompts.py` se ainda não baixar o prompt correto |
| 2 | Criar `prompts/bug_to_user_story_v2.yml` com técnicas do curso |
| 3 | Implementar/rodar `src/push_prompts.py` |
| 4 | `python src/evaluate.py` e iterar |
| 5 | `pytest tests/test_prompts.py` |

---

## Convenção de código (para este projeto)

Pedido explícito do time: **priorizar clareza para quem vem de PHP**, mesmo que não seja o estilo mais “pythônico”.

- Preferir funções com nomes claros e passos explícitos a atalhos com **métodos mágicos** (`__getattr__`, etc.) só para parecer elegante.
- Analogia rápida: um `.py` com funções no topo e um `if __name__ == "__main__":` no final é parecido com um script PHP que você inclui e chama funções — não precisa de classes se não ajudar.
- Quando usar bibliotecas (LangChain/LangSmith), siga os exemplos da documentação; o “simples” aqui é **legibilidade**, não reinventar a biblioteca.

---

## Onde anotar novas dicas

À medida que você for aprendendo (erros de API, truques no LangSmith, formato do YAML), acrescente novos arquivos em **`docs/`**, por exemplo:

- `docs/dicas-langsmith.md`
- `docs/erros-comuns.md`

Assim o histórico fica no repositório e não só na cabeça.

---

## Links úteis (oficiais)

- [Documentação LangSmith](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
