from pydantic_settings import BaseSettings


class ProviderSettings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str

    AUTHORIZE_URL: str = 'https://github.com/login/oauth/authorize'
    TOKEN_URL: str = 'https://github.com/login/oauth/access_token'
    USER_INFO: list = [
        (
            'https://api.github.com/user',
            lambda response: {
                'login': response['login']
            },
        ),
        (
            'https://api.github.com/user/emails',
            lambda response: {
                'email': response[0]['email']
            },
        ),
    ]

    SCOPES: list[str] = ['read:user', 'user:email']

    class Config:
        env_prefix = 'PROVIDER_'


class JWTSettings(BaseSettings):
    SECRET: str

    class Config:
        env_prefix = 'JWT_'
