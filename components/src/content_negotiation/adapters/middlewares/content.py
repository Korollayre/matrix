from falcon import Request, Response
from falcon.constants import MEDIA_HTML, MEDIA_JSON
from falcon.errors import HTTPBadRequest
from falcon.status_codes import HTTP_200, HTTP_BAD_REQUEST

from content_negotiation.adapters.utils import parse_priorities

HTML_TEMPLATE = (
    """
<!DOCTYPE html>
<html lang="{language}">

<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
</head>

<body>
<h1>{topic}</h1>
<p>{desc}</p>
</body>

</html>
    """
)


# pylint:disable=unused-argument
class ContentMiddleware:

    def process_request(self, request: Request, response: Response) -> None:
        if request.client_accepts(MEDIA_JSON) or (
                request.client_accepts(MEDIA_HTML)):
            return

        raise HTTPBadRequest(
            title='Unsupported content type.',
            description=(
                f'Supported content type - [{MEDIA_JSON}, {MEDIA_HTML}]'
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

        content_types = request.get_header('Accept')
        content_type = parse_priorities(content_types)
        if content_type == MEDIA_JSON:
            self.process_json(response)
        else:
            self.process_html(response)

    def process_json(self, response: Response) -> None:
        self._set_status(response)
        response.content_type = MEDIA_JSON
        response.media = response.context.result

    def process_html(self, response: Response) -> None:
        self._set_status(response)
        response.content_type = MEDIA_HTML
        response.text = HTML_TEMPLATE.format(**response.context.result)

    @staticmethod
    def _set_status(response: Response) -> None:
        response.status = response.context.result.pop('status', HTTP_200)
