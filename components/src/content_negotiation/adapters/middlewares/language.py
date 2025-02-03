from falcon import Request, Response
from falcon.errors import HTTPBadRequest
from falcon.status_codes import HTTP_BAD_REQUEST

from content_negotiation.adapters.constants import Languages


# pylint:disable=unused-argument
class LanguageMiddleware:

    def process_request(self, request: Request, response: Response) -> None:
        languages = request.get_header('Accept-Language')
        if languages:
            checks = [
                languages.find(Languages.EN),
                languages.find(Languages.RU),
            ]
            if any(el > -1 for el in checks):
                return

        raise HTTPBadRequest(
            title='Unsupported language.',
            description=(
                f'Supported languages - [{Languages.RU}, {Languages.EN}]'
            ),
            code=HTTP_BAD_REQUEST,
        )
