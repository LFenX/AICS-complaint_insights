"""Fail-closed token storage, atomic replacement and cross-process serialization."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import re
import secrets
import tempfile
import threading

from .config import ROOT

SERVER_PATH = ROOT / '.secrets/mcp-server.json'
REGISTRY_PATH = ROOT / '.secrets/mcp-token-registry.json'
IDENTITY = re.compile(r'[\w.-]{1,64}', re.UNICODE)
_lock = threading.RLock()
logger = logging.getLogger('insights.token_desk')


def _unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate JSON key')
        value[key] = item
    return value


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_unique)
    if not isinstance(value, dict):
        raise ValueError('JSON object required')
    return value


def validated_tokens(document: dict) -> dict[str, str]:
    issued = document.get('tokens')
    if not isinstance(issued, dict) or len(issued) > 1000:
        raise ValueError('invalid token store')
    if any(not isinstance(identity, str) or not IDENTITY.fullmatch(identity)
           or not isinstance(token, str) or len(token) < 32 or len(token) > 256
           or not token.isascii() or any(char.isspace() for char in token)
           for identity, token in issued.items()):
        raise ValueError('invalid token entry')
    if len(set(issued.values())) != len(issued):
        raise ValueError('duplicate token')
    return dict(issued)


def write_object(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def token_lock(server_path: Path):
    # One lock also covers metadata. Separate Python processes share this byte lock.
    with _lock:
        with server_path.with_suffix('.lock').open('a+b') as stream:
            stream.seek(0, os.SEEK_END)
            if stream.tell() == 0:
                stream.write(b'0')
                stream.flush()
            stream.seek(0)
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                stream.seek(0)
                if os.name == 'nt':
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _registry(path: Path) -> dict:
    registry = read_object(path) if path.exists() else {}
    if any(not isinstance(value, dict) for value in registry.values()):
        raise ValueError('invalid token metadata')
    return registry


def issue_token(identity: str, server_path: Path = SERVER_PATH, registry_path: Path = REGISTRY_PATH) -> str:
    if not IDENTITY.fullmatch(identity):
        raise ValueError('身份名称只能包含字母、数字、点、下划线和连字符，最长64个字符')
    with token_lock(server_path):
        server = read_object(server_path)  # Never recreate a missing/corrupt store.
        tokens = validated_tokens(server)
        registry = _registry(registry_path)
        if identity in tokens:
            raise ValueError('这个身份已经有令牌，请先撤销再重新发放')
        if len(tokens) >= 1000:
            raise ValueError('已达1000个身份上限，请先清理不再使用的身份')
        token = secrets.token_urlsafe(48)
        tokens[identity] = token
        registry[identity] = {'created_at': datetime.now(timezone.utc).isoformat(), 'prefix': token[:6]}
        # Metadata first: a failed config commit cannot accidentally authorize access.
        write_object(registry_path, registry)
        write_object(server_path, {**server, 'tokens': tokens})
        return token


def revoke_token(identity: str, server_path: Path = SERVER_PATH, registry_path: Path = REGISTRY_PATH) -> None:
    with token_lock(server_path):
        server = read_object(server_path)
        tokens = validated_tokens(server)
        if identity not in tokens:
            raise ValueError('没有这个身份，或该身份已经撤销')
        tokens.pop(identity)
        # Empty means deny everyone. Admin login is independent and can reissue.
        write_object(server_path, {**server, 'tokens': tokens})
        try:
            registry = _registry(registry_path)
            registry.pop(identity, None)
            write_object(registry_path, registry)
        except (OSError, ValueError, UnicodeError):
            logger.warning('{"action":"token.metadata","status":"repair_required"}')


def token_inventory(server_path: Path = SERVER_PATH, registry_path: Path = REGISTRY_PATH) -> tuple[list[dict], bool]:
    with token_lock(server_path):
        tokens = validated_tokens(read_object(server_path))
        metadata_available = True
        try:
            registry = _registry(registry_path)
        except (OSError, ValueError, UnicodeError):
            # Authorization is authoritative; broken display metadata cannot block revocation.
            registry = {}
            metadata_available = False
        rows = [{'identity': identity, 'prefix': token[:6],
                 'created_at': str(registry.get(identity, {}).get('created_at', '历史发放，时间未记录'))}
                for identity, token in sorted(tokens.items())]
        return rows, metadata_available


def token_rows(server_path: Path = SERVER_PATH, registry_path: Path = REGISTRY_PATH) -> list[dict]:
    return token_inventory(server_path, registry_path)[0]
