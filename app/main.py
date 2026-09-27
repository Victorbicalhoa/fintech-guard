import logging
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api.routes import api_router
from app.core.config import get_settings
from app.db.session import Base, engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # em produção isso vira migração (Alembic)
    Base.metadata.create_all(bind=engine)
    logger.info("Fintech Guard API iniciada (env=%s)", settings.environment)
    yield
    logger.info("Fintech Guard API encerrada")


app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description=(
        "API de apoio ao atendimento bancário: classifica a intenção do cliente "
        "e sinaliza risco de fraude/engenharia social."
    ),
    lifespan=lifespan,
    # sem Swagger em produção pra não publicar o mapa da API
    docs_url=None,
    redoc_url=None,
    openapi_url=None if settings.is_production else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    nonce = secrets.token_urlsafe(24)
    request.state.csp_nonce = nonce
    response = await call_next(request)
    docs = request.url.path in {"/docs", "/redoc"} and not settings.is_production
    external = " https://cdn.jsdelivr.net" if docs else ""
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'; "
        f"script-src 'self' 'nonce-{nonce}'{external}; "
        f"style-src 'self' 'nonce-{nonce}'{external}; "
        "img-src 'self' data:; connect-src 'self'; font-src 'self'; form-action 'self'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    # HSTS só é efetivado pelo navegador em HTTPS; TLS é obrigatório em produção.
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # o handler padrão devolve o input recebido dentro do erro; se o cliente
    # digitou o CPF no campo errado, o dado voltaria na resposta
    campos = [
        {"campo": ".".join(str(p) for p in e.get("loc", [])), "erro": e.get("msg", "")}
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Requisição inválida.", "erros": campos},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Erro não tratado em %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno do servidor."},
    )


app.include_router(api_router)


if not settings.is_production:
    from fastapi.openapi.docs import get_swagger_ui_html
    from fastapi.responses import HTMLResponse, RedirectResponse

    @app.get("/docs", include_in_schema=False)
    async def swagger(request: Request):
        html = get_swagger_ui_html(openapi_url=app.openapi_url, title="Fintech Guard - Swagger", swagger_favicon_url="/favicon.ico").body.decode()
        return HTMLResponse(html.replace("<script>", f'<script nonce="{request.state.csp_nonce}">'))

    @app.get("/redoc", include_in_schema=False)
    async def redoc(request: Request):
        # Uma única interface compatível com a CSP; mantém o endereço antigo.
        return RedirectResponse('/docs')
