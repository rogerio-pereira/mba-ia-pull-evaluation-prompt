Voce e um otimizador de prompts

Antes de tudo entenda o desafio
@README.md 

Tenho o prompt @prompts/bug_to_user_story_v2.yml , o objetivo dele e converter relatorios de bugs em User Stories

esse foi o resultado do @src/evaluate.py 
@/home/rogerio/.cursor/projects/home-rogerio-www-FullCycle-MBA-Desafios-Desafio02/terminals/1.txt:7-81 

entenda o prompt, e os exemplos em @datasets/bug_to_user_story.jsonl 

Regras
- Nao crie regras especificas somente para passar o teste do dataset, o prompt deve ser melhorado em geral
- Faca melhorias que melhorem o resultado geral, foque em F1, clareza, helpfulness, precisao, correctness
- Siga todas as regras em @README.md 

Passo a passo
1. Execute a avaliacao
2. Faca melhorias
3. faca o push do prompt `python src/push_prompts.py`
4. Execute a avaliacao `python src/evaluate.py `
5. Analise o resultado e compare com a iteracao anterior
6. Repita 2-5 (no maximo 3 vezes)