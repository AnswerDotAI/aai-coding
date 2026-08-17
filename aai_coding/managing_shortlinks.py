"""List, read, create, update, and delete Short.io links for one configured domain.

Configure the process with `SHORT_IO_API_KEY` and `SHORT_IO_DOMAIN`. The optional `SHORT_IO_API_URL` overrides the API root for testing or a compatible service. Secrets belong in the process environment, never function arguments, prompts, source code, or output.

Use `list_shortlinks` and `get_shortlink` for reads. `create_shortlink` creates one path. `update_shortlink` changes its destination, path, or title. Call `delete_shortlink(..., confirm=True)` only after the user explicitly approves that exact deletion.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from pyskills.core import allow

__all__ = [
    'ShortlinksError',
    'list_shortlinks',
    'get_shortlink',
    'create_shortlink',
    'update_shortlink',
    'delete_shortlink',
]


class ShortlinksError(RuntimeError):
    "Short.io configuration or API failure"


def normalize_shortlink_path(path):
    "Return a validated Short.io path without surrounding slashes"
    path = str(path).strip().strip('/')
    if not path or path in {'.', '..'} or '/../' in f'/{path}/' or any(c in path for c in '?#') or any(c.isspace() for c in path):
        raise ValueError(f'invalid shortlink path: {path!r}')
    return path


def validate_shortlink_url(url):
    "Return a validated HTTP(S) destination URL"
    url = str(url).strip()
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'} or not parsed.netloc:
        raise ValueError('shortlink destination must be an http(s) URL')
    return url


class ShortlinksClient:
    "Short.io client configured from the process environment"

    def __init__(self):
        self.api_key = os.environ.get('SHORT_IO_API_KEY')
        self.domain = os.environ.get('SHORT_IO_DOMAIN')
        self.api_url = os.environ.get('SHORT_IO_API_URL', 'https://api.short.io').rstrip('/')
        if not self.api_key: raise ShortlinksError('SHORT_IO_API_KEY is not configured')
        if not self.domain: raise ShortlinksError('SHORT_IO_DOMAIN is not configured')

    def request(self, method, path, query=None, body=None):
        "Send one authenticated API request and return decoded JSON"
        url = f'{self.api_url}{path}'
        if query: url = f'{url}?{urlencode(query)}'
        data = json.dumps(body).encode() if body is not None else None
        headers = {'Accept': 'application/json', 'Authorization': self.api_key}
        if data is not None: headers['Content-Type'] = 'application/json'
        try:
            with urlopen(Request(url, data=data, headers=headers, method=method), timeout=30) as response:
                raw = response.read()
                return json.loads(raw) if raw else None
        except HTTPError as e:
            raw = e.read()
            try:
                error = json.loads(raw)
                message = error.get('message') or error.get('error') or str(error)
            except (json.JSONDecodeError, AttributeError):
                message = raw.decode(errors='replace') or e.reason
            raise ShortlinksError(f'Short.io API returned {e.code}: {message}') from None
        except URLError as e:
            raise ShortlinksError(f'could not reach Short.io: {e.reason}') from None

    def domain_id(self):
        "Return the configured domain's Short.io ID"
        result = self.request('GET', '/api/domains', {'limit': 300, 'pattern': self.domain})
        domains = result if isinstance(result, list) else result.get('domains', result.get('data', []))
        for domain in domains:
            if domain.get('hostname') == self.domain: return domain['id']
        raise ShortlinksError(f'Short.io domain is unavailable: {self.domain}')


def list_shortlinks():
    "List every shortlink in `SHORT_IO_DOMAIN`"
    client = ShortlinksClient()
    domain_id = client.domain_id()
    links, token = [], None
    while True:
        query = {'domain_id': domain_id, 'limit': 150}
        if token: query['pageToken'] = token
        result = client.request('GET', '/api/links', query)
        links.extend(result.get('links', []))
        token = result.get('nextPageToken')
        if not token: return links


def get_shortlink(path):
    "Get one shortlink by path"
    client = ShortlinksClient()
    return client.request('GET', '/links/expand', {'domain': client.domain, 'path': normalize_shortlink_path(path)})


def create_shortlink(path, url, title=None):
    "Create `path` pointing to `url`"
    client = ShortlinksClient()
    body = {
        'domain': client.domain,
        'path': normalize_shortlink_path(path),
        'originalURL': validate_shortlink_url(url),
    }
    if title is not None: body['title'] = str(title)
    return client.request('POST', '/links', body=body)


def update_shortlink(path, *, url=None, new_path=None, title=None):
    "Update the destination, path, or title of one shortlink"
    if url is None and new_path is None and title is None: raise ValueError('provide at least one change')
    client = ShortlinksClient()
    link = client.request('GET', '/links/expand', {'domain': client.domain, 'path': normalize_shortlink_path(path)})
    body = {}
    if url is not None: body['originalURL'] = validate_shortlink_url(url)
    if new_path is not None: body['path'] = normalize_shortlink_path(new_path)
    if title is not None: body['title'] = str(title)
    return client.request('POST', f"/links/{link['idString']}", body=body)


def delete_shortlink(path, *, confirm=False):
    "Delete one shortlink after explicit confirmation"
    if not confirm: raise ValueError('shortlink deletion requires explicit confirmation')
    client = ShortlinksClient()
    link = client.request('GET', '/links/expand', {'domain': client.domain, 'path': normalize_shortlink_path(path)})
    return client.request('DELETE', f"/links/{link['idString']}")


allow(list_shortlinks, get_shortlink, create_shortlink, update_shortlink, delete_shortlink)
