# Por que parei antes de bater 0,9 (desistência e limites)

O desafio pedia repetir: melhorar o prompt → publicar no LangSmith → rodar a avaliação, até a **média das notas** passar de **0,9**. Eu **não cheguei nessa meta**.

---

## O que eu fiz até parar

- Trabalhei nos arquivos `src/pull_prompts.py`, `src/push_prompts.py`, `src/evaluate.py` para funcionar corretamente
- Trabalhei no arquivo `prompts/bug_to_user_story_v2.yml` (técnicas de prompt, exemplos, regras por tipo de bug).
- Usei `python src/push_prompts.py` para enviar o prompt para o Hub.
- Rodei `python src/evaluate.py` várias vezes para ver as notas.
- Repeti passos 2-4 até desistencia

As notas que apareceram no terminal ficaram na faixa de **0,74 a 0,80** (média geral), **abaixo de 0,9**. Não foi falta de saber *o que* fazer no fluxo (está no `README.md` e no `docs/01-primeiros-passos.md`); o que faltou foi **continuar pagando API** até talvez achar o ponto ideal.

---

## Por que parei (desistência)

O motivo principal foi **acabar o crédito na OpenAI**. Coloquei U$5 de credito e esgotei. 

Usei IA para melhorar o prompt em modo "Ralph Loop" entre commits `056e8fa70ff2eaedbb8a054fcb77580922a8e040` e `906de64ea58b53ba69082e555ed2bf5ba0c663a4`

Cada vez que você roda `evaluate.py`, o programa:

1. Gera uma resposta do modelo **principal** (no meu caso, `gpt-4o-mini`) para cada bug de teste.
2. Chama outro modelo (**mais caro**, o “juiz”, tipo `gpt-4o`) para dar nota em **vários critérios** por exemplo — isso está em `src/metrics.py`.

Ou seja: **uma avaliação completa gasta muitas chamadas**.

**Importante:** parar por crédito **não quer dizer** que o prompt não possa melhorar. Só significa que eu **não pude** continuar testando.

---

## Limites que eu notei (sem ser “culpa só minha”)

Coisas do **próprio desenho do exercício** que deixam a meta mais difícil ou “oscilante”:

- O script só usa os **10 primeiros** exemplos do dataset no LangSmith para calcular a média (ver `src/evaluate.py`). Não são os 15 do arquivo `jsonl` de uma vez — e a ordem dos exemplos no site pode não ser a mesma ordem do arquivo.
- Algumas notas que aparecem no terminal (**Helpfulness** e **Correctness**) **não vêm de um juiz separado**: são **médias** das outras notas. Detalhe em `docs/07-helpfulness-no-evaluate.md` e `docs/08-correctness-no-evaluate.md`.
- As notas **F1**, **Clarity** e **Precision** vêm de um **outro modelo** lendo sua resposta e comparando com um gabarito. Respostas “quase iguais” às vezes mudam a nota — é normal ter um pouco de variação.

Limites do **modelo barato** (`gpt-4o-mini`) gerando a user story:

- Às vezes ele manda **pouco texto** quando o gabarito quer mais seções (nota cai).
- Às vezes ele manda **seção a mais** quando o gabarito é bem curto (nota também pode cair).

Por isso melhorar o prompt é **tentativa e erro** — e erro custa API.

---

## Se alguém for continuar depois

1. Colocar crédito de novo **ou** configurar **Gemini** no `.env` (como no `.env.example`), se couber no seu plano.
2. Rodar de novo `push_prompts.py` e `evaluate.py`.
3. Olhar no LangSmith **o que** o modelo respondeu nos casos com nota baixa (tracing) e ajustar o YAML com calma.

---

## Onde ler mais técnico

- Como as métricas são calculadas no código: `src/evaluate.py` e `src/metrics.py`.
- Índice do que entra na avaliação (quantos exemplos, etc.): `docs/05-indice-exemplos-no-evaluate.md`.
- Moldes de user story e gabarito: `docs/06-moldes-gabarito-f1.md`.
