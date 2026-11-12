"""Confere os contratos OpenAPI por HTTP local, com banco vazio e chave efêmera."""
import argparse
from datetime import date
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time
import httpx

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {("/health", "get"), ("/auth/token", "post"), ("/auth/me", "get"),
            ("/predict", "post"), ("/predictions/{prediction_id}", "get")}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def resolve(doc, value):
    if "$ref" not in value:
        return value
    ref = value["$ref"]
    require(ref.startswith("#/"), "Referência externa inesperada.")
    result = doc
    for part in ref[2:].split("/"):
        result = result[part.replace("~1", "/").replace("~0", "~")]
    return result

def refs(doc, value):
    if isinstance(value, dict):
        if "$ref" in value:
            resolve(doc, value)
        for child in value.values():
            refs(doc, child)
    elif isinstance(value, list):
        for child in value:
            refs(doc, child)

def verify(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    runtime = ROOT / ".venv" / ("openapi-check-" + secrets.token_hex(6))
    runtime.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env.update(SECRET_KEY=secrets.token_urlsafe(64), ENVIRONMENT="development",
               DATABASE_URL="sqlite:///" + (runtime / "check.db").as_posix(),
               CORS_ORIGINS="http://localhost:3000", LOGIN_MAX_ATTEMPTS="5",
               LOGIN_WINDOW_SECONDS="300", PYTHONUTF8="1")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env["TP3_CHECK_PORT"] = str(port)
    env["TP3_CHECK_ROUTES"] = str(runtime / "routes.json")
    child = (
        "import os,json,uvicorn; from pathlib import Path; from app.main import app; "
        "routes=[{'path':r.path,'methods':sorted(r.methods or []),"
        "'include_in_schema':getattr(r,'include_in_schema',False)} "
        "for r in app.routes if hasattr(r,'methods')]; "
        "Path(os.environ['TP3_CHECK_ROUTES']).write_text(json.dumps(routes),encoding='utf-8'); "
        "uvicorn.run(app,host='127.0.0.1',port=int(os.environ['TP3_CHECK_PORT']),"
        "workers=1,proxy_headers=False,server_header=False)"
    )
    with (runtime / "server.log").open("w", encoding="utf-8") as log:
        process = subprocess.Popen([sys.executable, "-X", "utf8", "-c", child],
                                   cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
        try:
            with httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=5, trust_env=False) as client:
                deadline = time.monotonic() + 60
                while True:
                    require(process.poll() is None, "A API encerrou antes da validação.")
                    try:
                        health = client.get("/health")
                        if health.status_code == 200:
                            break
                    except httpx.TransportError:
                        pass
                    require(time.monotonic() < deadline, "Timeout ao iniciar a API.")
                    time.sleep(0.25)
                docs = client.get("/docs")
                api = client.get("/openapi.json")
            require(health.json()["database"] == "up", "Banco indisponível.")
            require(docs.status_code == api.status_code == 200, "Documentação indisponível.")
            require("text/html" in docs.headers.get("content-type", ""), "Swagger sem HTML.")
            require("/openapi.json" in docs.text and "SwaggerUIBundle" in docs.text, "HTML incompleto.")
            doc = api.json()
            refs(doc, doc)
            methods = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
            operations = {(p, m) for p, item in doc["paths"].items() for m in item if m in methods}
            routes = json.loads((runtime / "routes.json").read_text(encoding="utf-8"))
            registered = {(r["path"], m.lower()) for r in routes if r["include_in_schema"]
                          for m in r["methods"] if m.lower() in methods}
            require(operations == registered == EXPECTED, "Cobertura de operações divergente.")
            contracts = []
            for path, method in sorted(operations):
                op = doc["paths"][path][method]
                require(op.get("summary") and op.get("description"), "Descrição ausente.")
                response = op["responses"]["200"]["content"]["application/json"]["schema"]
                output_schema = resolve(doc, response)
                require(output_schema.get("properties"), "Schema de saída ausente.")
                bodies = {}
                for media, details in op.get("requestBody", {}).get("content", {}).items():
                    schema = resolve(doc, details["schema"])
                    bodies[media] = {"schema": details["schema"], "required": schema.get("required", []),
                                    "properties": schema.get("properties", {}),
                                    "additionalProperties": schema.get("additionalProperties")}
                if method == "post":
                    require(bodies and all(b["additionalProperties"] is False for b in bodies.values()),
                            "Body sem schema ou permitindo campos extras.")
                if path in {"/auth/me", "/predict", "/predictions/{prediction_id}"}:
                    require(op.get("security"), "Autenticação não descrita.")
                contracts.append({"method": method.upper(), "path": path, "summary": op["summary"],
                                  "request": bodies, "parameters": op.get("parameters", []),
                                  "response_200": response, "response_fields": sorted(output_schema["properties"]),
                                  "documented_statuses": sorted(op["responses"]),
                                  "security": op.get("security", [])})
            require(doc["components"]["schemas"]["PredictRequest"]["properties"]["message"]["maxLength"] == 1000,
                    "Limite de mensagem divergente.")
            require(doc["components"]["schemas"]["Channel"]["enum"] == ["chat", "whatsapp", "email", "telefone"],
                    "Canais divergentes.")
            summary = {"review_date": date.today().isoformat(), "status": "passed",
                       "transport": "HTTP em 127.0.0.1, porta efêmera; servidor encerrado ao final",
                       "environment": "development", "health_status": health.status_code,
                       "docs_status": docs.status_code, "openapi_status": api.status_code,
                       "openapi_version": doc["openapi"], "operation_count": len(contracts),
                       "all_registered_business_routes_documented": True,
                       "all_local_schema_references_resolved": True, "contracts": contracts,
                       "limits": ["Conferência de contratos declarados; não é scan de segurança.",
                                  "HTML Swagger disponível; renderização visual não foi repetida.",
                                  "Não verifica implantação pública, TLS nem API adversária."]}
            for name, obj in [("openapi.json", doc), ("openapi-validacao.json", summary)]:
                (output / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({k: summary[k] for k in ["status", "docs_status", "openapi_status", "operation_count"]}))
            return summary
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/TP3/revisao_20261111")
    verify(parser.parse_args().output)
