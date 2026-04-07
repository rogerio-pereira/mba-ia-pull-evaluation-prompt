# "Correctness" no `evaluate.py`

Em `src/evaluate.py`:

```text
avg_correctness = (avg_f1 + avg_precision) / 2
```

**Correctness** é a média entre **F1** (alinhamento com o gabarito / completude) e **Precision** (foco, fatos corretos, menos alucinação).

Para subir as duas ao mesmo tempo, o prompt precisa:

1. **Cobrir cada tema do relato** (evita omissão → melhor F1).
2. **Reutilizar dados do bug** (endpoints, HTTP, números, aspas) sem inventar (→ melhor Precision).
3. **Escolher o molhe certo** (simples vs médio vs complexo) para o tamanho e quantidade de frentes do bug.

A revisão do `bug_to_user_story_v2.yml` prioriza o PASSO A de cobertura + regra explícita contra “resposta curta demais”.
