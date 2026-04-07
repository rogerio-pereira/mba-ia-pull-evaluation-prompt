# Moldes do gabarito (F1)

O arquivo `datasets/bug_to_user_story.jsonl` não usa um único formato. Há três famílias:

1. **Simples** — uma frase “Como… eu quero… para que…” + `Critérios de Aceitação:` com `Dado/Quando/Então/E`.
2. **Médio** — igual ao simples + seções extras (`Contexto Técnico:`, `Contexto do Bug:`, `Critérios Técnicos:`, etc.) conforme o tipo de bug.
3. **Complexo** — blocos com `=== USER STORY PRINCIPAL ===`, `=== CRITÉRIOS DE ACEITAÇÃO ===` (A., B., C.), `=== CRITÉRIOS TÉCNICOS ===`, `=== CONTEXTO DO BUG ===`, `=== TASKS TÉCNICAS SUGERIDAS ===` e às vezes `=== MÉTRICAS DE SUCESSO ===`.

Forçar sempre o molde simples faz o juiz de F1 comparar com um gabarito muito mais longo e estruturado nos itens médios/complexos, derrubando recall. O `bug_to_user_story_v2.yml` foi ajustado para **escolher o molde** conforme o tamanho e o tipo de relato.

**Clareza:** o juiz `evaluate_clarity` pontua organização, linguagem simples, baixa ambiguidade e concisão. Por isso o YAML inclui a seção "CLAREZA" com regras de espaçamento entre blocos, ordem Dado/Quando/Então, frases curtas e evitar redundância entre seções.
