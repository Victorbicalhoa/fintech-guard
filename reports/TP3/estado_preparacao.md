# Estado da preparação do TP3 - 14/10/2026

## Concluído
- Cópia do repositório entregue no GitHub preparada na pasta TP3, base 649f5c43f91f4b2fa0bbdadfb357061175760377.
- Notebook, script de regressão simples/múltipla, baseline, métricas e diagnósticos implementados, ainda sem execução concluída.
- Pergunta de classificação e planejamento T2 redigidos; campos do adversário explicitamente pendentes.
- Dataset conferido: 603 mensagens, seis classes; hash igual ao TP2.
- Validação sintática de scripts e células aprovada; notebook estruturalmente válido.
- Os 43 testes herdados passaram em 9,07 segundos com o novo arquivo de testes de regressão excluído da coleta.
- Nenhuma alteração em app/, data/, notebooks/TP1, notebooks/TP2, reports/TP1 ou reports/TP2.

## Bloqueios e limitações desta execução
A política de Controle de Aplicativo do Windows bloqueou a DLL importada por
`scipy.optimize._highspy._core`. A execução do notebook falhou na primeira célula;
a suíte completa também falhou na coleta do novo módulo de testes. Não há R², RMSE,
resíduos ou gráficos calculados/validados. Os quatro testes novos ainda não passaram.
Não considerar esta preparação uma entrega pronta para o Moodle.

A criação da branch feat/tp3-dados também foi bloqueada ao escrever em .git/refs,
mesmo após a concessão de permissão. Os arquivos permanecem locais, não commitados,
na cópia recém-clonada em main. Nenhum push, PR ou alteração remota foi realizado.

## Retomada em ambiente autorizado
Usar uma instalação Python/SciPy permitida pela política do Windows, sem desativar
os controles de segurança. Confirmar a instalação com o responsável pelo ambiente,
se necessário. Na raiz do TP3:

```powershell
.venv/Scripts/python.exe -c "from scipy import stats; import sklearn; print('Importações OK')"
.venv/Scripts/python.exe -m scripts.execute_tp3_notebook
.venv/Scripts/python.exe -m pytest tests/ -v -p no:cacheprovider
```

Após sucesso, conferir tabelas e gráficos, escrever interpretações específicas dos
resíduos observados, verificar consistência das métricas e remover a nota de execução
pendente do notebook. O arquivo protocol.json registra versões e parâmetros; o manifesto
permite conferir a partição. Revisar dados, saídas e documentos antes de commit/publicação.

A ausência de adversário e URL ainda impede finalizar o plano conjunto; o integrante B
permanece responsável por essa informação, CI, OpenAPI e auditoria final do TP3.
