from flask import Flask, request

from proxy import ProxyProc

import settings

app = Flask('__main__')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    proxy_proc = ProxyProc(
        '{}{}'.format(settings.TARGET_URL, path),
        request)
    return proxy_proc.get_response()


app.run(host=settings.HOST, port=settings.PORT)
