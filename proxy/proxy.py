import re

from bs4 import BeautifulSoup
from flask import Response
from requests import get

import settings


class ProxyProc(object):
    _res = None

    def __init__(self, path, request):
        self.path = path
        self.request = request

    def get_response(self):
        self._proc_request()
        return self._proc_response()

    def _proc_request(self):
        headers = {
            'User-Agent': self.request.headers.get('User-Agent'),
            'Accept': self.request.headers.get('Accept'),
        }
        self._res = get(url=self.path, headers=headers)

    def _proc_response(self):
        content = self._handle(self._res.content)
        return Response(
            response=content,
            status=self._res.status_code)

    def _handle(self, content):
        try:
            # Wrapped to try-except statement just for handle
            # requests only with html
            soup = BeautifulSoup(content.decode())
        except Exception:
            return content

        # Replace site url with local proxy url
        pattern = r'^https://habr.com/'
        links = soup.find_all('a', attrs={'href': re.compile(pattern)})
        for link in links:
            replaced = re.sub(pattern, settings.SITE_NAME, link.get('href'))
            link['href'] = replaced

        # Added trade mark for all six-length words
        for text in soup.find_all(text=True):
            if re.search(r'\b\w{6}\b', text):
                replaced = re.sub(r'\b\w{6}\b', r'\g<0>&trade;', text)
                text.replaceWith(BeautifulSoup(replaced, 'html.parser'))

        return str(soup).encode()

