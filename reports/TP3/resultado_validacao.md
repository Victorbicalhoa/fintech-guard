# Validação do TP3 - Dados e IA

Execução em Linux no GitHub Actions concluída em 14/10/2026.

- Execução: https://github.com/Victorbicalhoa/fintech-guard/actions/runs/38582165258
- Branch: `feat/tp3-dados`, no fork `Victorbicalhoa/fintech-guard`.
- Commit executado: `be6cc45fe7aac090fbf7928b9283f7f53451e7b8`.
- Base upstream: `649f5c43f91f4b2fa0bbdadfb357061175760377`.
- Resultado: **47 testes aprovados**, 14 avisos de dependências, 7,23 segundos.
- Notebook: sete células de código executadas, três figuras incorporadas, sem erros.
- Artefato: `11903233076`; SHA-256 `0ae34fb2d58a3a7098bbe6a2885603db9de47620879ef60ad74c16a1bb11312d`, conferido no download.
- Ambiente efetivo: Python 3.13.16, SciPy 1.18.1, scikit-learn 1.9.1; demais versões em `ci/environment.txt`.

## Resultados de avaliação interna
482 mensagens de treino e 121 de avaliação, semente 42, mesmas partições nos modelos.

| Modelo | R² | RMSE (caracteres) |
|---|---:|---:|
| Média do treino | -0,00182 | 372,33 |
| Regressão simples | 0,99877 | 13,05 |
| Regressão múltipla | 0,99946 | 8,61 |

O erro da múltipla é menor nesta divisão. Como alvo e preditores medem a extensão do mesmo
texto, esse desempenho não valida detecção de fraude nem classificação de intenções.
O Q-Q mostra desvios na cauda positiva; os dois textos mais longos da avaliação permanecem
subestimados. As interpretações específicas foram adicionadas apenas em células Markdown,
depois da revisão das figuras; código e saídas numéricas do artefato foram preservados.

## Escopo e integridade
Os quatro testes novos de Dados passaram com os 43 herdados. Dados e evidências TP1/TP2,
bem como a API, permaneceram inalterados. O repositório do colega não recebeu mudanças.
Não foi treinado classificador, nem realizado pentest ou configurada proteção de merge.
O plano conjunto ainda depende da identificação do adversário e URL autorizada pelo integrante B.

## Histórico do ambiente local
O Windows bloqueou a extensão nativa do SciPy. O pacote local foi comparado com o wheel
oficial e era idêntico; não se desativou o Controle Inteligente de Aplicativos. A execução
comprovada é a do runner Linux, e não a do Windows. As evidências foram baixadas para TP3.
O primeiro disparo falhou antes de criar job por configuração de contexto no workflow;
a correção do cache resultou na execução aprovada acima.

O JSON `ci/validation.json` contém a checagem automatizada original. Este documento registra
a revisão posterior das três figuras e das métricas. Logs e JUnit estão em `ci/`.
