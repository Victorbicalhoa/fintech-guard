# Evidências da revisão local — 11/11/2026

Base: main integrada 2f71cb77f80a8d1e13f8738d3cd59bd20b67baff, com os ajustes locais
descritos em [revisao_feedback.md](../revisao_feedback.md). No momento da execução, os ajustes eram locais. Veja o estado posterior em [publicação](../publicacao_github.md).

- [execution.json](execution.json): comandos, códigos de saída, commit-base e hashes das fontes executadas.
- [environment.txt](environment.txt): versões do ambiente Python usado.
- [notebook.log](notebook.log): execução completa, sete células de código e três imagens incorporadas.
- [pytest.txt](pytest.txt) e [pytest.xml](pytest.xml): 95 casos aprovados, sem falhas/erros/skips.
- [validation.json](validation.json) e [validation.log](validation.log): reprodução do dataset e das métricas.
- [openapi.json](openapi.json): schema obtido da API local em execução.
- [openapi-validacao.json](openapi-validacao.json): cinco operações, entrada/saída, autenticação declarada e disponibilidade HTTP.
- [sha256.json](sha256.json): integridade dos arquivos desta revisão; o próprio manifesto é excluído.

Os logs substituem caminhos absolutos pessoais por `<workspace>`. Os resultados da API
foram obtidos com banco de teste vazio e chave efêmera, sem publicar credenciais.
Os relatórios antigos permanecem nos respectivos diretórios, com suas datas originais.
