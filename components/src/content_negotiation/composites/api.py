from falcon import App

from content_negotiation.adapters.controllers import Example
from content_negotiation.adapters.middlewares import (
    CompressionMiddleware,
    ContentMiddleware,
    LanguageMiddleware,
)

app = App(
    middleware=[
        CompressionMiddleware(),
        ContentMiddleware(),
        LanguageMiddleware(),
    ],
)

app.add_route('/api', Example())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    with make_server('127.0.0.1', 8000, app) as httpd:
        print("Serving HTTP on port http://127.0.0.1:8000/api")
        httpd.serve_forever()
