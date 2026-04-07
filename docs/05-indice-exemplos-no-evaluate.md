# Índice [5/10] e ordem dos exemplos

O `evaluate.py` imprime `[5/10]` = **5º exemplo** entre os **10 primeiros** retornados por `client.list_examples(...)`.

Essa ordem **costuma** ser a ordem em que os exemplos foram **criados** no dataset (muitas vezes igual à ordem das linhas do `datasets/bug_to_user_story.jsonl`), mas **não é garantido** pela API. Se quiser ter certeza de qual bug é o “quinto”:

1. Abra o projeto no **LangSmith** e a lista de exemplos do dataset de avaliação.
2. Confira o **5º item** da lista (ou o ID do exemplo ligado ao trace).

Para melhorar o **F1** de um caso específico, compare no trace: **resposta do modelo** × **campo `reference`** naquele exemplo — o F1 penaliza omissão de partes importantes do gabarito e conteúdo inventado.
