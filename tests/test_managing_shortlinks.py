import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse

import pytest

from aai_coding.managing_shortlinks import (
    ShortlinksError,
    create_shortlink,
    delete_shortlink,
    get_shortlink,
    list_shortlinks,
    update_shortlink,
)


@pytest.fixture
def shortio(monkeypatch):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args): pass

        def reply(self, body, status=200):
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def record(self):
            n = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(n)) if n else None
            requests.append((self.command, self.path, body, self.headers.get('Authorization')))
            return body

        def do_GET(self):
            self.record()
            u = urlparse(self.path)
            q = parse_qs(u.query)
            if u.path == '/api/domains': return self.reply([
                {'id': 9, 'hostname': 'other.example'},
                {'id': 42, 'hostname': 'link.answer.ai'},
            ])
            if u.path == '/api/links':
                assert q['domain_id'] == ['42']
                if q.get('pageToken') == ['next']:
                    return self.reply({'links': [{'path': 'wiki'}], 'nextPageToken': None})
                return self.reply({'links': [{'path': 'discord'}], 'nextPageToken': 'next'})
            if u.path == '/links/expand':
                assert q['domain'] == ['link.answer.ai']
                return self.reply({'path': q['path'][0], 'idString': 'lnk_123', 'originalURL': 'https://old.example'})
            return self.reply({'error': 'missing'}, 404)

        def do_POST(self):
            body = self.record()
            if self.path == '/links': return self.reply({'idString': 'lnk_new', **body})
            if self.path == '/links/lnk_123': return self.reply({'idString': 'lnk_123', **body})
            return self.reply({'error': 'missing'}, 404)

        def do_DELETE(self):
            self.record()
            if self.path == '/links/lnk_123': return self.reply({'success': True})
            return self.reply({'error': 'missing'}, 404)

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setenv('SHORT_IO_API_KEY', 'test-key')
    monkeypatch.setenv('SHORT_IO_DOMAIN', 'link.answer.ai')
    monkeypatch.setenv('SHORT_IO_API_URL', f'http://127.0.0.1:{server.server_port}')
    yield requests
    server.shutdown()
    thread.join()


def test_shortlinks_crud(shortio):
    assert [x['path'] for x in list_shortlinks()] == ['discord', 'wiki']
    assert get_shortlink('dm/jeremy')['idString'] == 'lnk_123'
    created = create_shortlink('dm/jeremy', 'https://discord.com/users/123', title='Jeremy')
    assert created['path'] == 'dm/jeremy'
    updated = update_shortlink('dm/jeremy', url='https://discord.com/users/456', new_path='dm/j')
    assert updated['originalURL'] == 'https://discord.com/users/456'
    assert updated['path'] == 'dm/j'
    assert delete_shortlink('dm/jeremy', confirm=True) == {'success': True}
    assert {r[3] for r in shortio} == {'test-key'}
    assert sum(path.startswith('/api/domains') for _, path, _, _ in shortio) == 1


def test_shortlinks_safety(shortio, monkeypatch):
    with pytest.raises(ValueError, match='confirmation'): delete_shortlink('wiki')
    with pytest.raises(ValueError, match='http'): create_shortlink('wiki', 'javascript:alert(1)')
    with pytest.raises(ValueError, match='path'): create_shortlink('../wiki', 'https://example.com')
    with pytest.raises(ValueError, match='change'): update_shortlink('wiki')
    monkeypatch.delenv('SHORT_IO_API_KEY')
    with pytest.raises(ShortlinksError, match='SHORT_IO_API_KEY'): list_shortlinks()
