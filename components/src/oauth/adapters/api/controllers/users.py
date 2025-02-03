import secrets
from dataclasses import dataclass
from urllib.parse import urlencode

import jwt
import requests
from falcon import Request, Response
from falcon.errors import HTTPBadRequest
from falcon.status_codes import HTTP_200, HTTP_303

from oauth.adapters.api.models import OnGetCallback
from oauth.adapters.api.settings import JWTSettings, ProviderSettings
from oauth.applications import interfacies


def get_user_ident_from_token(request: Request, secret: str) -> str:
    str_token = request.get_header('Authorization').split()[1]
    bytes_token = str.encode(str_token)
    token_data = jwt.decode(
        bytes_token,
        key=secret,
        algorithms='HS256',
    )

    return token_data.get('sub')


# pylint:disable=unused-argument
@dataclass
class Users:
    service: interfacies.Users

    provider_settings: ProviderSettings
    jwt_settings: JWTSettings

    def on_get_authorize(self, request: Request, response: Response):
        oauth2_state = secrets.token_urlsafe(16)
        response.context.oauth2_state = oauth2_state

        query_params = urlencode(
            {
                'client_id': self.provider_settings.CLIENT_ID,
                'redirect_uri': 'http://127.0.0.1:8000/api/auth/callback',
                'response_type': 'code',
                'scope': ' '.join(self.provider_settings.SCOPES),
                'state': oauth2_state,
            }
        )
        query = f'{self.provider_settings.AUTHORIZE_URL}?{query_params}'

        response.status = HTTP_303
        response.set_header('Location', query)

    def on_get_callback(self, request: Request, response: Response):
        params: OnGetCallback = OnGetCallback(**request.params)

        oauth2_token = self._provider_authorize(params)
        user_info = self._provider_get_user_info(oauth2_token)

        user = self.service.login(**user_info)
        response.set_header(
            'Authorization',
            jwt.encode(
                {
                    'sub': user.ident,
                    'login': user.login,
                    'email': user.email,
                },
                key=self.jwt_settings.SECRET,
                algorithm='HS256',
            ),
        )

    def _provider_authorize(self, params: OnGetCallback) -> str:
        data = {
            'client_id': self.provider_settings.CLIENT_ID,
            'client_secret': self.provider_settings.CLIENT_SECRET,
            'code': params.code,
            'grant_type': 'authorization_code',
        }
        response = requests.post(
            self.provider_settings.TOKEN_URL,
            data=data,
            headers={'Accept': 'application/json'},
            timeout=5
        )
        if f'{response.status_code} {response.reason}' != HTTP_200:
            raise HTTPBadRequest

        oauth2_token = response.json().get('access_token')
        if not oauth2_token:
            raise HTTPBadRequest
        return oauth2_token

    def _provider_get_user_info(self, oauth2_token: str) -> dict:
        info = {}
        for url, method in self.provider_settings.USER_INFO:
            response = requests.get(
                url,
                headers={
                    'Authorization': 'Bearer ' + oauth2_token,
                    'Accept': 'application/json',
                },
                timeout=5
            )
            if f'{response.status_code} {response.reason}' != HTTP_200:
                raise HTTPBadRequest
            info.update(method(response.json()))
        return info

    def on_get_profile(self, request: Request, response: Response):
        ident = get_user_ident_from_token(request, self.jwt_settings.SECRET)

        user = self.service.get(ident)
        response.media = {
            'ident': user.ident,
            'email': user.email,
            'login': user.login,
        }
