# Controles e testes locais do TP2

## Persistência e ownership

`User` e `PredictionLog` agora usam SQLModel. As consultas usam `select()` e `Session.exec()`, com parâmetros vinculados pelo ORM; não há SQL textual nas rotas, inclusive no health check. SQLAlchemy continua como dependência subjacente do SQLModel.

Foram preservados nomes, colunas e tabelas do esquema anterior. Um teste cria o esquema SQLAlchemy anterior, grava registros e verifica leitura e nova gravação pelo SQLModel sem alterar as colunas. Não foi aplicado comando destrutivo ao banco local. Isso é compatibilidade com o esquema conhecido, não uma ferramenta de migração de bancos arbitrariamente modificados.

`POST /predict` mantém os campos anteriores e acrescenta `prediction_id`. `GET /predictions/{prediction_id}` exige JWT e filtra simultaneamente ID e `username` do usuário autenticado. Outro usuário recebe o mesmo 404 de um ID inexistente. A resposta não inclui mensagem, hash, senha ou identidade do proprietário. Sem token, retorna 401.

A ownership reaproveita o username persistido, único e sem endpoint de renomeação nesta aplicação. Antes de adicionar renomeação, exclusão/reutilização de contas, migrar a associação para uma chave imutável de usuário e preservar a atribuição histórica.

## Entradas

`PredictRequest` e o formulário `LoginRequest` usam `ConfigDict(extra="forbid")`. Campo adicional no JSON de predição ou formulário de autenticação resulta em 422. Os campos usuais do formulário OAuth2 estão declarados para manter compatibilidade com o Swagger. A validação de entrada é distinta dos modelos SQLModel de persistência e dos modelos de saída.

## Headers e documentação

Middleware inclui HSTS, X-Frame-Options, X-Content-Type-Options e CSP, além dos headers existentes. HSTS é enviado também no ambiente local, mas navegadores só o aplicam via HTTPS; a implantação de produção exige TLS.

A CSP usa `default-src 'none'`, bloqueia enquadramento, objetos e alteração da base, restringe conexões e formulários à própria origem e autoriza blocos inline somente com nonce aleatório por resposta. A página inicial recebe o nonce em seus scripts e estilos. O Swagger de desenvolvimento permite os assets de `cdn.jsdelivr.net` e recebe nonce no script de inicialização; `/redoc` redireciona para `/docs` para manter uma interface de documentação compatível com a política. A documentação continua desabilitada em produção.

Os testes conferem headers e nonces no HTML, mas não substituem teste visual completo no navegador nem auditoria ZAP.

## CORS

`CORS_ORIGINS` define origens explícitas separadas por vírgula, por exemplo `http://localhost:3000`. Curingas e valores com caminhos são rejeitados na configuração. Preflight autorizado retorna 200 com a origem correspondente; origem não permitida retorna 400 sem `Access-Control-Allow-Origin`. Respostas a requisições simples de origem não permitida também omitem a autorização CORS. CORS é uma política do navegador, não uma substituição da autenticação.

## Limite de autenticação

O padrão é **cinco falhas por IP em uma janela móvel de 300 segundos**. Após cinco respostas 401, a próxima tentativa retorna 429, inclusive se as credenciais forem válidas. Um login bem-sucedido antes do bloqueio zera o contador. A configuração usa `LOGIN_MAX_ATTEMPTS` e `LOGIN_WINDOW_SECONDS`.

Cinco falhas permitem alguns erros de digitação e limitam tentativas automatizadas repetidas; cinco minutos desaceleram a repetição sem bloqueio permanente. São valores iniciais para o projeto, a revisar segundo tráfego e falsos bloqueios. IP compartilhado pode bloquear vários usuários. O contador é em memória por processo: múltiplos workers/reinício exigem armazenamento compartilhado e política apropriada. Não se confia automaticamente em `X-Forwarded-For` enviado pelo cliente.

## Evidência de validação

Com as dependências de desenvolvimento instaladas, executar `python -m pytest tests/ -q -p no:cacheprovider`.

Resultado local: **28 testes aprovados nesta branch de API** (34 na cópia integrada com os seis testes de atributos da EDA), incluindo:

- Recurso sem token: 401.
- Proprietário: 200; outro usuário ou ID inexistente: 404.
- Campo extra no JSON e no formulário: 422; predição inválida não grava histórico.
- Headers em sucesso, 401 e 404; nonces distintos e presentes na interface/documentação.
- CORS autorizado e negado, com rejeição de curingas.
- Bloqueio com 429 após cinco falhas.
- Compatibilidade com esquema SQLAlchemy anterior e consulta com entrada semelhante a SQL injection tratada como valor literal.

SQLModel 0.0.24 foi adicionado às dependências. A checagem de compatibilidade dos 78 pacotes instalados passou.

## Escopo ainda pendente

Esta evidência é de testes locais, não um relatório de pentest. Não foi executado ZAP nem produzido relatório de findings nesta alteração. Esses itens e a implantação devem ser conferidos em conjunto com o integrante B antes da entrega completa.
