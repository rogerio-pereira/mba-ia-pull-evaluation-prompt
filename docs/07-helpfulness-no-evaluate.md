# O que é "Helpfulness" no `evaluate.py`?

Neste projeto, **não existe um juiz LLM separado** chamado Helpfulness.

Em `src/evaluate.py`:

```text
avg_helpfulness = (avg_clarity + avg_precision) / 2
```

Ou seja, **subir Helpfulness** = subir **Clarity** e/ou **Precision** ao mesmo tempo.

- **Precision** (ver `evaluate_precision` em `metrics.py`): ausência de alucinação, foco na tarefa, correção factual vs. referência.
- **Clareza:** organização, linguagem, ambiguidade, concisão.

O prompt `bug_to_user_story_v2.yml` inclui a seção **UTILIDADE E FOCO** para reforçar: sem divagação, sem fatos inventados, só o que o bug sustenta — o que tende a melhorar Precision e, com isso, Helpfulness.
