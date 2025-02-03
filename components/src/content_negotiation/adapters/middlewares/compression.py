import gzip

import brotli
from falcon import Request, Response
from falcon.errors import HTTPBadRequest
from falcon.status_codes import HTTP_BAD_REQUEST

from content_negotiation.adapters.utils import parse_priorities


class CompressionTypes:
    """Поддерживаемые типы сжатия."""

    GZIP: str = 'gzip'
    BROTLI: str = 'br'


# pylint:disable=unused-argument
class CompressionMiddleware:

    def process_request(self, request: Request, response: Response) -> None:
        encodings = request.get_header('Accept-Encoding')
        if encodings:
            checks = [
                encodings.find(CompressionTypes.GZIP),
                encodings.find(CompressionTypes.BROTLI),
            ]
            if any(el > -1 for el in checks):
                return

        raise HTTPBadRequest(
            title='Unsupported compression.',
            description=(
                f'Supported compressions - '
                f'[{CompressionTypes.GZIP}, {CompressionTypes.BROTLI}]'
            ),
            code=HTTP_BAD_REQUEST,
        )

    def process_response(
        self,
        request: Request,
        response: Response,
        resource: object,
        req_succeeded: bool,
    ) -> None:
        if not hasattr(response.context, 'result'):
            return

        encodings = request.get_header('Accept-Encoding')
        compression = parse_priorities(encodings)
        if compression == CompressionTypes.BROTLI:
            self._compress_brotli(response)
        else:
            self._compress_gzip(response)

    @staticmethod
    def _compress_brotli(response: Response) -> None:
        data = response.render_body()
        if data is None:
            return
        response.data = brotli.compress(data)
        response.text = None
        response.set_header('Content-Encoding', CompressionTypes.BROTLI)

    @staticmethod
    def _compress_gzip(response: Response) -> None:
        data = response.render_body()
        if data is None:
            return
        response.data = gzip.compress(data)
        response.text = None
        response.set_header('Content-Encoding', CompressionTypes.GZIP)
