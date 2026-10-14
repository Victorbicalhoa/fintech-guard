# TP3 - Entrega do integrante A (Dados e IA)

Base: upstream `franciscocostadev/fintech-guard`, commit
`649f5c43f91f4b2fa0bbdadfb357061175760377`, obtido em 14/10/2026.
A cópia local TP2 foi preservada; a base entregue no GitHub inclui as correções finais da dupla.

## Evidências
| Rubrica de Dados | Evidência |
|---|---|
| Pré-processamento, LinearRegression e múltipla | `notebooks/TP3/security/01_regressao_e_transicao.ipynb` e `scripts/tp3_regression.py` |
| R², RMSE, resíduos e Q-Q | Notebook executado; `regression/metrics.csv`; `figures/` |
| Limitações da regressão para intenções | Seção 6 do notebook; `pergunta_classificacao.md` |
| Classes, distribuição e ML supervisionado | `pergunta_classificacao.md` |
| Candidato e features para T2 | `planejamento_T2.md` |

## Reprodução no PowerShell, a partir da raiz
```powershell
.venv/Scripts/python.exe -m pip install -r requirements-tp3-dados.txt
.venv/Scripts/python.exe -m scripts.execute_tp3_notebook
.venv/Scripts/python.exe -m pytest tests/ -v -p no:cacheprovider
```
Se o ambiente foi instalado com uv e não contém pip, usar
`uv pip install --python .venv/Scripts/python.exe -r requirements-tp3-dados.txt`.
O notebook também encontra a raiz quando iniciado na própria pasta. O script é a implementação
compartilhada; o notebook mostra pipelines ajustados, tabelas e interpretações.

## Escopo e pendências
Somente Dados e IA foram implementados. A API, workflow, configuração de merge, auditoria final,
OpenAPI e identificação do adversário cabem ao integrante B. Executar testes existentes para
verificar regressões não equivale a concluir a auditoria do TP3. Nenhum classificador foi treinado.

TP1 e TP2 continuam em suas pastas. Os CSVs originais e tratados não são modificados pelo TP3.
O relatório `planejamento_T2.md` lista explicitamente campos ainda pendentes do plano conjunto.

## Execução comprovada
Notebook e 47 testes aprovados no GitHub Actions. Ver [resultado e limitações](resultado_validacao.md). O bloqueio local do Windows permanece; usar o workflow para reproduzir nesse contexto.
