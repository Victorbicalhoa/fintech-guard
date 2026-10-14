# Execução de Dados do TP3 no fork

Publicação autorizada pelo usuário. O workflow executa em pushes exclusivamente na branch
`feat/tp3-dados` de `Victorbicalhoa/fintech-guard`, sem alterar main ou o upstream.
O gatilho manual também está definido, mas o botão só fica disponível se o workflow existir
na branch padrão. Não dependemos dele para esta validação.

O runner Ubuntu 24.04 instala Python 3.13 e requirements-tp3-dados.txt, executa o notebook,
a suíte completa e scripts.verify_tp3_evidence. Token somente leitura, sem secrets ou deploy.
O artefato tp3-dados-<run_id>-<tentativa> guarda notebook, figuras, métricas, manifesto,
versões, commit, logs e JUnit por 14 dias. Também há upload em falhas: exigir execução verde
e ci/validation.json; revisar os gráficos e interpretações antes de entregar.

As notas de bloqueio local são históricas. Os outputs Linux não demonstram execução Windows.
Este workflow não substitui o CI de segurança/proteção de merge do integrante B.
