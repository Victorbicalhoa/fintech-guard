# Pergunta de classificação - Fintech Guard
Integrante A | TP3 | 14/10/2026

## Tarefa e unidade de análise
Dado o texto de uma mensagem, há indícios de ameaça de engenharia social ou o conteúdo é benigno?
A unidade é uma mensagem; a entrada é texto, e a saída planejada é uma classe de segurança.
O objetivo é apoiar triagem, sem autorizar transações ou declarar que uma pessoa cometeu fraude.
O rótulo descreve o conteúdo no dataset, não prova a intenção real do remetente.

O enunciado usa “intenções de atendimento”. Nosso recorte é a intenção maliciosa/tipo de ameaça,
coerente com o desafio Fintech Guard. Não confundimos essas classes com fatura, cancelamento ou
investimentos. BANKING77 tem 77 intenções de atendimento e permanece uma tarefa complementar;
não será unido ao dataset de segurança. Se o professor exigir especificamente roteamento bancário,
essa tarefa deve ser formalizada e avaliada separadamente com BANKING77.

## Classes e distribuição
Fonte: dataset de segurança documentado em `docs/dataset_security.md`; 624 registros originais,
15 exclusões por conflitos e seis duplicatas removidas, resultando em 603 mensagens em inglês.

| Classe original | Definição operacional no projeto | n | % |
|---|---|---:|---:|
| NOT-Malicious General Class | Conteúdo benigno segundo o dataset | 171 | 28,36 |
| Phishing | Indução a fornecer informações ou acessar conteúdo fraudulento | 110 | 18,24 |
| Scareware | Medo ou urgência para induzir ação | 100 | 16,58 |
| Baiting | Prêmio/benefício usado como isca | 80 | 13,27 |
| Malware | Indução a instalar ou executar conteúdo malicioso | 77 | 12,77 |
| Pretexting | Pretexto ou identidade alegada para obter cooperação | 65 | 10,78 |
| Total | | 603 | 100,00 |

**Decisão proposta para T2:** classificação binária principal, benigno (171; 28,36%) versus
ameaça (432; 71,64%), agrupando as outras cinco categorias. Ameaça será a classe positiva.
Isso responde à triagem e reduz a fragmentação dos exemplos. Não elimina desbalanceamento
nem resolve a diferença de domínio/idioma. Manteremos os seis rótulos originais para análise
de erros por subtipo; uma comparação multiclasse será secundária, caso a validação por classe
seja viável. A base tem apenas 65 exemplos de Pretexting, não 65 exemplos de cada cenário real.

## Por que aprendizado supervisionado
Há exemplos rotulados e o conteúdo envolve combinações de termos e contexto, além do tamanho.
No TP2, Mann–Whitney resultou em p≈0,1912, com efeito pequeno; não rejeitar H₀ não estabelece
um limiar útil nem prova igualdade. O TP3 aproxima comprimento com regressão, uma variável
contínua e estruturalmente ligada à contagem de palavras. R²/RMSE não medem detecção de ameaça.

Regressão linear de códigos de classe imporia ordem e distâncias arbitrárias, sem garantir
probabilidades válidas. TF-IDF com regressão logística poderá aprender associações de termos
com rótulos, avaliadas por recall, precisão e F1 por classe. Regressão logística é um método
estatístico de classificação supervisionada: a escolha não é “ML contra estatística”, mas um
objetivo categórico adequado em lugar da regressão contínua e da análise descritiva isolada.

## Limites e critério de evidência
Licença ainda não esclarecida, amostra pequena em inglês, possível dependência por templates
e ambiguidade Phishing/Pretexting limitam a inferência. A EDA expôs a base completa; o futuro
teste interno não será chamado de intocado desde a origem. Será necessária avaliação externa
independente, com condições de uso e anotação documentadas, próxima do atendimento bancário
em português. Nenhum classificador foi treinado no TP3.
