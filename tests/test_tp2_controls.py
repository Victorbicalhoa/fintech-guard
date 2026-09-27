import re
import pytest
from pydantic import ValidationError
from sqlmodel import SQLModel, select

from app.main import settings
from app.core.config import Settings
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.models.user import User
from app.models.audit import PredictionLog
from app.schemas.predict import PredictRequest
from app.services import rate_limit
from tests.conftest import USERNAME, PASSWORD


def test_resource_requires_token(client):
    assert client.get('/predictions/1').status_code == 401


def test_owner_and_other_user_and_missing_resource(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    created = client.post('/predict', headers=headers, json={'message': 'cartao bloqueado'})
    assert created.status_code == 200
    resource_id = created.json()['prediction_id']
    own = client.get(f'/predictions/{resource_id}', headers=headers)
    assert own.status_code == 200
    assert own.json()['id'] == resource_id
    assert not {'username', 'message_hash', 'message', 'hashed_password'} & own.json().keys()
    with SessionLocal() as db:
        db.add(User(username='outro-usuario', hashed_password=hash_password(PASSWORD)))
        db.commit()
    other_token, _ = create_access_token(subject='outro-usuario', scopes=['analyst'])
    other_headers = {'Authorization': f'Bearer {other_token}'}
    denied = client.get(f'/predictions/{resource_id}', headers=other_headers)
    missing = client.get('/predictions/99999999', headers=other_headers)
    assert denied.status_code == missing.status_code == 404
    assert denied.json() == missing.json()


def test_extra_body_is_rejected_without_creating_record(client, token):
    with SessionLocal() as db:
        before = len(db.exec(select(PredictionLog)).all())
    result = client.post('/predict', headers={'Authorization': f'Bearer {token}'},
                         json={'message': 'ola', 'username': 'outro-usuario'})
    assert result.status_code == 422
    with SessionLocal() as db:
        assert len(db.exec(select(PredictionLog)).all()) == before


def test_extra_login_field_rejected(client):
    response = client.post('/auth/token', data={'username': USERNAME, 'password': PASSWORD, 'admin': 'true'})
    assert response.status_code == 422


@pytest.mark.parametrize('path', ['/health', '/not-found', '/predictions/1'])
def test_headers_on_success_and_errors(client, path):
    response = client.get(path)
    assert response.headers['strict-transport-security'] == 'max-age=31536000; includeSubDomains'
    assert response.headers['x-frame-options'] == 'DENY'
    assert response.headers['x-content-type-options'] == 'nosniff'
    assert "frame-ancestors 'none'" in response.headers['content-security-policy']
    assert "'unsafe-inline'" not in response.headers['content-security-policy']


@pytest.mark.parametrize('path', ['/', '/docs'])
def test_inline_scripts_have_per_response_nonce(client, path):
    first, second = client.get(path), client.get(path)
    nonce = re.search(r"'nonce-([^']+)'", first.headers['content-security-policy']).group(1)
    assert f'nonce="{nonce}"' in first.text
    assert first.headers['content-security-policy'] != second.headers['content-security-policy']
    assert '<script>' not in first.text
    assert '<style>' not in first.text


def test_cors_allowlist(client):
    origin = settings.cors_origins_list[0]
    headers = {'Origin': origin, 'Access-Control-Request-Method': 'POST',
               'Access-Control-Request-Headers': 'Authorization,Content-Type'}
    allowed = client.request('OPTIONS', '/predict', headers=headers)
    assert allowed.status_code == 200
    assert allowed.headers['access-control-allow-origin'] == origin
    headers['Origin'] = 'https://untrusted.example'
    denied = client.request('OPTIONS', '/predict', headers=headers)
    assert denied.status_code == 400
    assert 'access-control-allow-origin' not in denied.headers
    actual = client.get('/health', headers={'Origin': headers['Origin']})
    assert 'access-control-allow-origin' not in actual.headers


def test_auth_rate_limit_429(client):
    rate_limit.reset('127.0.0.1')
    try:
        for _ in range(settings.login_max_attempts):
            assert client.post('/auth/token', data={'username': 'missing-user', 'password': 'wrong'}).status_code == 401
        assert client.post('/auth/token', data={'username': USERNAME, 'password': PASSWORD}).status_code == 429
    finally:
        rate_limit.reset('127.0.0.1')


def test_sqlmodel_and_injection_like_username():
    assert issubclass(User, SQLModel) and issubclass(PredictionLog, SQLModel)
    with SessionLocal() as db:
        assert db.exec(select(User).where(User.username == "' OR 1=1 --")).first() is None
    with pytest.raises(ValidationError):
        PredictRequest(message='ola', unexpected=True)


@pytest.mark.parametrize('origin', ['*', 'https://*.example', 'https://example/path'])
def test_cors_rejects_wildcards_and_paths(origin):
    with pytest.raises(ValidationError):
        Settings(_env_file=None, secret_key='test-only-secret-with-at-least-32-chars', cors_origins=origin)


def test_legacy_sqlalchemy_schema_compatibility():
    from datetime import datetime, timezone
    from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, Float, create_engine, inspect
    from sqlmodel import Session
    legacy = MetaData()
    users = Table('users', legacy,
        Column('id', Integer, primary_key=True), Column('username', String(64), unique=True, index=True, nullable=False),
        Column('hashed_password', String(128), nullable=False), Column('full_name', String(120)),
        Column('role', String(32), nullable=False), Column('is_active', Boolean, nullable=False),
        Column('created_at', DateTime(timezone=True), nullable=False))
    logs = Table('prediction_logs', legacy,
        Column('id', Integer, primary_key=True), Column('username', String(64), index=True, nullable=False),
        Column('message_hash', String(64), nullable=False), Column('message_length', Integer, nullable=False),
        Column('predicted_intent', String(64), nullable=False), Column('confidence', Float, nullable=False),
        Column('risk_level', String(16), nullable=False), Column('created_at', DateTime(timezone=True), index=True, nullable=False))
    engine = create_engine('sqlite://')
    try:
        legacy.create_all(engine)
        before = {table: inspect(engine).get_columns(table) for table in ['users', 'prediction_logs']}
        with engine.begin() as conn:
            conn.execute(users.insert().values(id=1,username='legacy-user',hashed_password='test-hash',role='analyst',is_active=True,created_at=datetime.now(timezone.utc)))
            conn.execute(logs.insert().values(id=1,username='legacy-user',message_hash='a'*64,message_length=10,predicted_intent='test',confidence=.5,risk_level='low',created_at=datetime.now(timezone.utc)))
        SQLModel.metadata.create_all(engine)
        with Session(engine) as db:
            assert db.get(User, 1).username == 'legacy-user'
            assert db.get(PredictionLog, 1).message_length == 10
            db.add(PredictionLog(username='legacy-user',message_hash='b'*64,message_length=20,predicted_intent='test',confidence=.8,risk_level='low'))
            db.commit()
            assert len(db.exec(select(PredictionLog)).all()) == 2
        for table, columns in before.items():
            assert [(c['name'],str(c['type']),c['nullable']) for c in columns] == [(c['name'],str(c['type']),c['nullable']) for c in inspect(engine).get_columns(table)]
    finally:
        engine.dispose()
