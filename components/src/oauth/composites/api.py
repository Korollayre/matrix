from oauth.adapters import api
from oauth.applications import services


class Settings:
    provider = api.settings.ProviderSettings()
    jwt = api.settings.JWTSettings()


class Apps:
    users = services.Users()


app = api.create_app(
    provider_settings=Settings.provider,
    jwt_settings=Settings.jwt,
    users_service=Apps.users,
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    with make_server('127.0.0.1', 8000, app) as httpd:
        print("Serving HTTP on port http://127.0.0.1:8000/api/users/authorize")
        httpd.serve_forever()
