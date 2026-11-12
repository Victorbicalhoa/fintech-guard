# TP3 — Índice de evidências da entrega

Revisão: **11/11/2026**. Base integrada: [2f71cb7](https://github.com/franciscocostadev/fintech-guard/commit/2f71cb77f80a8d1e13f8738d3cd59bd20b67baff).
A contribuição de Dados entrou na main pelo [PR #3](https://github.com/franciscocostadev/fintech-guard/pull/3),
integrado em **23/10/2026**. A segurança foi integrada posteriormente pelo integrante B.
A revisão de 11/11, conferida em 12/11, segue na branch `fix/tp3-feedback` para revisão por PR.
Consulte a [conferência das 12 rubricas](rubricas_TP3.md), com a seleção original do Rubricator.

## Comece por estes arquivos

1. [Notebook executado de regressão](../../notebooks/TP3/security/01_regressao_e_transicao.ipynb).
2. [Pergunta de classificação](pergunta_classificacao.md) e [PDF de duas páginas](pergunta_classificacao.pdf).
3. [Planejamento T2](planejamento_T2.md).
4. [Resposta técnica ao feedback e pendências](revisao_feedback.md).

## Mapa dos requisitos

| Item | Onde conferir | Evidência |
|---|---|---|
| Pré-processamento e LinearRegression simples/múltipla | Notebook, seções 2 e 3 | Construção e fit explícitos de SimpleImputer → StandardScaler → LinearRegression; mesmos 482/121 registros |
| R² e RMSE interpretados | Notebook, seção 4; [metrics.csv](regression/metrics.csv) | Cálculo explícito e comparação com a média do treino |
| Residual plot e Q-Q plot | Notebook, seção 5; [resíduos](figures/residuos.png) e [Q-Q](figures/qq.png) | Gráficos incorporados com interpretação |
| Limitações para classificação de intenções | Notebook, seção 6; pergunta de classificação | Saída contínua, classes nominais e redundância entre atributos/alvo |
| Classes, distribuição e aprendizado supervisionado | [Pergunta de classificação](pergunta_classificacao.md) | 603 mensagens; seis classes; binária principal proposta: 171 benignas/432 ameaças |
| Modelo candidato e feature engineering | Plano T2, seções 2–5 | TF-IDF + LogisticRegression; comparação com LinearSVC; divisão, métricas e contrato futuro |
| Pelo menos cinco casos de segurança e aprovação da suíte atual | [pytest.txt](revisao_20261111/pytest.txt), [JUnit](revisao_20261111/pytest.xml) | 95 aprovados, zero falhas/erros/ignorados; 14 avisos de dependências |
| GitHub Actions | [workflow](../../.github/workflows/security-tests.yml) e [run da main](https://github.com/franciscocostadev/fintech-guard/actions/runs/40040833325) | 95 testes aprovados no commit base; regras de merge documentadas pelo integrante B |
| Findings Medium/High | [Auditoria final](../../docs/auditoria-final-tp3.md) | Auditoria de 23/10: nenhum pendente; não foi realizado novo ZAP nesta revisão |
| OpenAPI em execução | [JSON exportado](revisao_20261111/openapi.json) e [validação](revisao_20261111/openapi-validacao.json) | HTTP 200 em /docs e /openapi.json; cinco operações com contratos, referências resolvidas |
| Adversário e URL/IP | Plano T2, seção 6; auditoria, seção 7 | **PENDENTE**, ainda não definidos pela dupla |

## Resultados do experimento de regressão

| Modelo | R² na avaliação | RMSE em caracteres |
|---|---:|---:|
| Média do treino | -0,00182 | 372,33 |
| Simples | 0,99877 | 13,05 |
| Múltipla | 0,99946 | 8,61 |

O alvo é comprimento do texto; os preditores também descrevem sua extensão.
O desempenho alto reflete uma relação estrutural e **não mede detecção de fraude**.
O protocolo original foi preservado; a revisão tornou o código explícito nas células.
A partição pedagógica já foi examinada e não constitui teste externo do classificador futuro.

## Reprodução a partir da raiz

~~~powershell
python -m pip install -r requirements-dev.txt
python -m scripts.execute_tp3_notebook
python -m pytest tests/ -v -p no:cacheprovider --junitxml=reports/TP3/revisao_20261111/pytest.xml
python -m scripts.verify_tp3_evidence --test-report reports/TP3/revisao_20261111/pytest.xml --output reports/TP3/revisao_20261111/validation.json
python -m scripts.verify_tp3_openapi --output reports/TP3/revisao_20261111
~~~

Use uma nova pasta de evidências ao registrar outra data, para preservar o histórico.
O verificador OpenAPI sobe apenas uma API local em 127.0.0.1, com chave efêmera e banco vazio,
e encerra o servidor ao final. Ele valida os contratos declarados; não executa pentest nem
repete a renderização visual do Swagger no navegador. A captura histórica permanece na auditoria.

## Histórico e responsabilidades

- [Validações anteriores e atual](resultado_validacao.md): 47 testes em 14/10, 58 em 17–18/10 e 95 na versão integrada.
- [Publicação e merge](publicacao_github.md): origem dos commits e estado desta revisão.
- [Execução de 11/11](revisao_20261111/execution.json), [ambiente](revisao_20261111/environment.txt) e [hashes](revisao_20261111/sha256.json).

Integrante A: dados, regressão, pergunta de classificação e planejamento de ML.
Integrante B: API, CI de segurança, auditoria e disponibilização do alvo.
Identificação do adversário e autorização precisam ser consolidadas pela dupla.
Nenhum classificador foi treinado e nenhum ataque adversarial foi realizado nesta revisão.
