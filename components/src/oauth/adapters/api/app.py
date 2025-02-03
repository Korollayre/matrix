from falcon import App

from oauth.adapters.api import controllers, settings
from oauth.applications import interfacies


def create_app(
    provider_settings: settings.ProviderSettings,
    jwt_settings: settings.JWTSettings,
    users_service: interfacies.Users,
) -> App:

    app = App()

    c_users = controllers.Users(
        service=users_service,
        provider_settings=provider_settings,
        jwt_settings=jwt_settings,
    )
    app.add_route('/api/users/authorize', c_users, suffix='authorize')
    app.add_route('/api/auth/callback', c_users, suffix='callback')
    app.add_route('/api/users/profile', c_users, suffix='profile')

    return app
