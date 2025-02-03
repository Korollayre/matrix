from falcon import Request, Response

from .constants import Languages
from .utils import parse_priorities

RU_RESULT = {
    'title': 'Какой-то заголовок',
    'topic': 'Какой-то топик',
    'desc': 'Какое-то описание',
}

EN_RESULT = {
    'title': 'Some title',
    'topic': 'Some topic',
    'desc': 'Some desc',
}


class Example:

    def on_get(self, request: Request, response: Response):
        languages = request.get_header('Accept-Language')
        language = parse_priorities(languages)

        if language == Languages.EN:
            result = EN_RESULT
        else:
            result = RU_RESULT
        result.update(language=language)

        response.context.result = result
