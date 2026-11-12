# Publicação e integração do TP3

Atualização documental: **12/11/2026**.

## Entrega anterior já integrada

- Fork/branch: Victorbicalhoa/fintech-guard, `feat/tp3-dados`.
- Head da entrega de Dados: `a0cabd21b8f327bee5dd849f607dd08412a237b2`.
- [PR #3](https://github.com/franciscocostadev/fintech-guard/pull/3): aberto em 18/10 e integrado em **23/10/2026**, às 20h08 (America/Sao_Paulo).
- Merge: [f0deb02](https://github.com/franciscocostadev/fintech-guard/commit/f0deb02bad2d647c8b714d2c453f0fc1f4c069f5).
- A main inspecionada em 11/11 está em [2f71cb7](https://github.com/franciscocostadev/fintech-guard/commit/2f71cb77f80a8d1e13f8738d3cd59bd20b67baff) e contém os artefatos de Dados.
- A main do fork ainda aponta para `0d5ee24`; abrir apenas a página inicial do fork não mostra a entrega da branch de TP3.

As mensagens históricas de falha 403 se referiam à tentativa automática de abrir o PR.
O PR foi aberto posteriormente e integrado; aquele bloqueio não é o estado atual da entrega.

## Validação remota

- [Dados no fork, 18/10](https://github.com/Victorbicalhoa/fintech-guard/actions/runs/39140016363):
  commit `a0cabd2`, notebook e **58 testes aprovados**.
- [Suíte integrada na main, 23/10](https://github.com/franciscocostadev/fintech-guard/actions/runs/40040833325):
  commit `2f71cb7`, **95 testes aprovados**, 14 avisos de dependências.

## Revisão do feedback para novo PR

A revisão de 11/11 explicita pipelines e métricas no notebook, organiza os requisitos em um
índice, atualiza o planejamento e reúne nova validação de notebook, pytest e OpenAPI.
A revisão segue na branch `fix/tp3-feedback` do fork, baseada na main integrada.
O [comparativo da revisão](https://github.com/franciscocostadev/fintech-guard/compare/main...Victorbicalhoa:fintech-guard:fix/tp3-feedback)
identifica os arquivos alterados. O PR #3 permanece como histórico da entrega original.
Confira o estado de integração e os checks no novo PR antes de entregar ao Moodle.

A revisão do feedback não permite identificar qual commit foi consultado pelo avaliador.
O repositório informado é o do Francisco; não foram informados data ou snapshot da avaliação.

## Preservação de evidências

`ci/`, `local_validation/` e `ci_20261018/` registram execuções anteriores e permanecem intactos.
O ZIP de evidências de 18/10 registrado anteriormente possui SHA-256
`9ed8620db54bb46195aa8d8373bcdddb9f1fa90cc02483e01f5a4ef81c8edd36`.
A execução nova está em [revisao_20261111/](revisao_20261111/).
Adversário, URL/IP e autorização continuam pendentes.
