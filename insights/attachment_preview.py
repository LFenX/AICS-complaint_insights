"""Bounded, inert previews generated from verified local attachment copies."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import warnings

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
import zstandard

register_heif_opener()
TEXT_LIMIT = 256_000
IMAGE_TYPES = {'image/jpeg', 'image/jpg', 'image/png', 'image/heic', 'image/gif', 'image/webp', 'image/bmp'}


def file_kind(name: str, content_type: str):
    suffix = Path(name).suffix.lower()
    if suffix in {'.log', '.txt', '.clog', '.zst'} or content_type.startswith('text/'):
        return 'log'
    if content_type in IMAGE_TYPES or suffix in {'.jpg', '.jpeg', '.png', '.heic', '.gif', '.webp', '.bmp'}:
        return 'image'
    return 'document'


def detected_type(prefix: bytes):
    if prefix.startswith(b'\xff\xd8\xff'):
        return 'image/jpeg'
    if prefix.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if prefix.startswith((b'GIF87a', b'GIF89a')):
        return 'image/gif'
    if prefix.startswith(b'RIFF') and prefix[8:12] == b'WEBP':
        return 'image/webp'
    if prefix.startswith(b'BM'):
        return 'image/bmp'
    if prefix.startswith(b'%PDF-'):
        return 'application/pdf'
    return None


def decode_text(raw: bytes):
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return raw.decode('utf-16', errors='replace')
    if raw.count(b'\0') / max(1, len(raw)) > .03:
        raise ValueError('BINARY_NOT_TEXT')
    for encoding in ('utf-8-sig', 'gb18030'):
        try:
            return raw.decode(encoding)
        except UnicodeError:
            pass
    return raw.decode('utf-8', errors='replace')


def prepare_files(directory: Path, expected: list[dict], *, snapshot_sha256: str | None = None,
                  rebuild_previews: bool = False):
    manifest_path = directory / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'files': {}}
    if snapshot_sha256 and manifest.get('source_snapshot_sha256') != snapshot_sha256:
        raise ValueError('attachment manifest belongs to another source snapshot')
    result = []
    for original in expected:
        p = original['payload']
        key = str(p['id'])
        source = manifest['files'].get(key, {})
        kind = file_kind(p.get('filename') or '', p.get('content_type') or '')
        item = {'id': key, 'mail_pk': str(p['message_pk']), 'name': p.get('filename') or 'attachment',
                'content_type': p.get('content_type') or 'application/octet-stream', 'kind': kind,
                'size': int(source.get('size') or p.get('size_bytes') or 0), 'ready': False,
                'status': source.get('status') or 'pending', 'sha256': source.get('sha256'),
                'error': source.get('error'), 'preview_type': None, 'preview_head': ''}
        path = directory / (key + '.bin')
        if source.get('status') == 'ready' and path.is_file() and source.get('identity_verified'):
            # The fetcher already compared the original attachment ID's content hash.
            # Report generation verifies its independently retained SHA-256 again.
            from hashlib import file_digest
            with path.open('rb') as f:
                actual = file_digest(f, 'sha256').hexdigest()
            if actual != source.get('sha256'):
                item.update(status='failed', error='LOCAL_DIGEST_MISMATCH')
                result.append(item)
                continue
            with path.open('rb') as f:
                detected = detected_type(f.read(32))
            if detected:
                item['detected_content_type'] = detected
                kind = file_kind(item['name'], detected)
                item['kind'] = kind
            item.update(ready=True, status='ready')
            try:
                if rebuild_previews:
                    # These are generated derivatives owned by this adapter.
                    # Candidate builds must derive them from the verified original,
                    # rather than certify an unproven or interrupted cache entry.
                    for suffix in ('.jpg', '.txt', '.pdf.jpg'):
                        (directory / (key + suffix)).unlink(missing_ok=True)
                if kind == 'image':
                    dest = directory / (key + '.jpg')
                    if not dest.is_file():
                        with warnings.catch_warnings():
                            warnings.simplefilter('error', Image.DecompressionBombWarning)
                            with Image.open(path, formats=['JPEG', 'PNG', 'GIF', 'WEBP', 'BMP', 'HEIF']) as img:
                                if img.width * img.height > 40_000_000:
                                    raise ValueError('IMAGE_PIXEL_LIMIT')
                                img = ImageOps.exif_transpose(img)
                                img.thumbnail((1800, 1800))
                                img.convert('RGB').save(dest, 'JPEG', quality=88)
                    item['preview_type'] = 'image'
                elif kind == 'log':
                    dest = directory / (key + '.txt')
                    if not dest.is_file():
                        with path.open('rb') as f:
                            magic = f.read(4)
                            f.seek(0)
                            if magic == b'\x28\xb5\x2f\xfd':
                                with zstandard.ZstdDecompressor().stream_reader(f) as stream:
                                    raw = stream.read(TEXT_LIMIT + 1)
                            else:
                                raw = f.read(TEXT_LIMIT + 1)
                        truncated = len(raw) > TEXT_LIMIT
                        text = decode_text(raw[:TEXT_LIMIT])
                        if truncated:
                            text += '\n\n[预览截断至256KB；下载原文件查看全部内容]'
                        dest.write_text(text, encoding='utf-8')
                    item['preview_type'] = 'text'
                    with dest.open(encoding='utf-8') as f:
                        item['preview_head'] = f.read(180)
                elif (item.get('detected_content_type') or item['content_type']) == 'application/pdf':
                    item['preview_type'] = 'pdf'
                    dest = directory / (key + '.pdf.jpg')
                    if not dest.is_file():
                        renderer = shutil.which('pdftoppm')
                        if renderer:
                            try:
                                subprocess.run([renderer, '-f', '1', '-singlefile', '-scale-to', '1600',
                                                '-jpeg', str(path), str(directory / (key + '.pdf'))],
                                               timeout=20, check=True, capture_output=True)
                            except (OSError, subprocess.SubprocessError):
                                item['preview_error'] = 'PDF_FIRST_PAGE_RENDER_FAILED'
                        else:
                            item['preview_error'] = 'PDF_RENDERER_UNAVAILABLE'
                    item['preview_image'] = dest.is_file()
                elif item['content_type'].startswith('video/'):
                    item['preview_type'] = 'video'
                else:
                    item['preview_type'] = 'metadata'
            except (OSError, ValueError, Image.DecompressionBombWarning, Image.DecompressionBombError, zstandard.ZstdError) as error:
                item['preview_type'] = 'metadata'
                item['preview_error'] = type(error).__name__
        result.append(item)
    return result
