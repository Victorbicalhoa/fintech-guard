# Revisão do feedback do TP3 — 11/11/2026

## Diagnóstico da entrega

O repositório avaliado foi **franciscocostadev/fintech-guard**, conforme confirmação do integrante A.
Na consulta de 11/11, a main estava em [2f71cb7](https://github.com/franciscocostadev/fintech-guard/commit/2f71cb77f80a8d1e13f8738d3cd59bd20b67baff).
O [PR #3](https://github.com/franciscocostadev/fintech-guard/pull/3) foi integrado em 23/10/2026
e contém a contribuição de Dados. O notebook, a pergunta de classificação e o planejamento
já existem nessa main. A comparação dos arquivos locais publicados no PR confirmou que o
trabalho foi preservado.

Sem a data/commit efetivamente examinado na avaliação, não é possível concluir por que os
artefatos foram apontados como ausentes. A documentação interna ainda registrava estados
anteriores à publicação e o README precisava oferecer um caminho direto para as evidências.

## Ajustes desta revisão

- Notebook: tornar explícitos nas células a construção de Pipeline, o pré-processamento,
  o ajuste de LinearRegression simples/múltipla, a predição e os cálculos de R² e RMSE.
  O script reproduzível permanece como referência, com comparações que detectam divergências.
- Preservar a divisão de 482 registros de treino e 121 de avaliação, as features e os
  resultados anteriores. A regressão é um exercício com alvo numérico derivado, não um
  classificador de fraude. Não houve treinamento de classificação.
- Reexecutar todas as células e preservar tabelas, métricas e os três gráficos.
- Criar um índice visível no README e corrigir os registros de preparação/publicação.
- Detalhar o contrato futuro com a API: a saída binária benigno/ameaça não pode substituir
  silenciosamente intent, hoje documentado como intenção BANKING77.
- Consolidar a execução atual dos 95 testes e conferir os schemas por HTTP local.
  A implementação da API do integrante B foi preservada.

Veja também a [conferência das 12 rubricas](rubricas_TP3.md), comparada ao print em 12/11.

## Enunciado e rubricas: onde verificar

| Exigência | Evidência e resultado |
|---|---|
| Pré-processamento → regressão simples → múltipla | [Notebook executado](../../notebooks/TP3/security/01_regressao_e_transicao.ipynb), seção 3; imputer e scaler ajustados apenas no treino |
| R² e RMSE calculados e contextualizados | Notebook, seção 4; [métricas](regression/metrics.csv). Simples: R² ≈ 0,99877, RMSE ≈ 13,05 caracteres; múltipla: R² ≈ 0,99946, RMSE ≈ 8,61 caracteres |
| Residual plot e Q-Q plot | Figuras incorporadas no notebook; diagnósticos interpretados sem presumir normalidade |
| Limitações para classificação | Notebook e [pergunta de classificação](pergunta_classificacao.md): redundância estrutural, alvo contínuo versus categorias, ausência de evidência de detecção de ameaças |
| Pelo menos cinco testes de segurança | [Execução completa](revisao_20261111/pytest.txt): autenticação, BOLA, entradas inválidas e rate limiting presentes; 95 casos aprovados no total |
| GitHub Actions automático | [.github/workflows/security-tests.yml](../../.github/workflows/security-tests.yml); [execução da main](https://github.com/franciscocostadev/fintech-guard/actions/runs/40040833325) aprovada. Ruleset ativo reconferido em 12/11: exige PR e check security-tests; [snapshot](revisao_rubricas_20261112/ruleset-main.json) |
| Todos os testes aprovados | 95 aprovados, zero falhas, erros ou skips, 14 avisos de depreciação; [JUnit](revisao_20261111/pytest.xml) |
| Pergunta, classes e distribuição | [Documento Markdown](pergunta_classificacao.md) e [PDF](pergunta_classificacao.pdf); 603 mensagens, seis rótulos originais e proposta binária explícita |
| Justificativa para aprendizado supervisionado | Documento de pergunta: uso dos rótulos/texto, limitações dos atributos de comprimento e necessidade de avaliação por classe |
| Algoritmo e feature engineering no plano T2 | [Planejamento](planejamento_T2.md): TF-IDF + regressão logística, comparação com LinearSVC, referência majoritária e prevenção de vazamento |
| Colega adversário e URL/IP | **PENDENTE**, ainda não definidos; manter campos abertos, conforme confirmação do integrante A |
| Findings ZAP Medium/High | [Auditoria final de B](../../docs/auditoria-final-tp3.md) e seus relatórios registram zero Medium/High no scan final de 23/10. Nenhum novo scan foi executado nesta revisão |
| OpenAPI acessível e schemas documentados | [Validação HTTP](revisao_20261111/openapi-validacao.json) e [OpenAPI exportado](revisao_20261111/openapi.json): /docs e /openapi.json com 200, cinco operações com schemas, referências resolvidas e autenticação declarada |

O [índice do TP3](README.md) reúne os entregáveis e comandos de reprodução.
A [validação numérica](revisao_20261111/validation.json) reconfirmou 603 registros,
seis classes, 363 predições (três modelos × 121 casos) e seis linhas de métricas.
A validação automática exige também a leitura humana das interpretações e dos limites metodológicos.

## Limites desta conferência

A resposta HTML de /docs e os contratos JSON foram verificados em execução; a renderização
visual do Swagger no navegador não foi repetida. A conferência não demonstra disponibilidade
pública, TLS, ausência de vulnerabilidades nem autorização de ataque. Os testes automatizados
e o scan passivo documentado têm alcances distintos.

O R² muito alto decorre da forte relação entre medidas do próprio texto. Não demonstra
capacidade de classificar intenções. A proposta de segurança binária continua separada do
roteamento bancário e precisa de alinhamento na integração com B.

## Pendências e passagem para o TP4

1. Revisar o PR da branch `fix/tp3-feedback` e referenciar o commit integrado na entrega.
2. A dupla definir o colega adversário, a URL/IP e a autorização/escopo/janela do pentest.
3. Alinhar o recorte de classificação e o contrato de classes/scores com B, preservando
   a distinção entre ameaças e intenções bancárias.
4. Antes de treinar, fechar protocolo de separação, métricas e critérios de seleção,
   conforme o planejamento; não usar o conjunto de avaliação para escolher o modelo.

A documentação e o notebook de Dados atendem aos itens verificáveis nesta revisão.
O plano conjunto permanece incompleto enquanto adversário e URL/IP não forem definidos.
As execuções acima são de 11/11. A conferência das rubricas e a preparação da publicação por novo PR são de 12/11.
