from dataclasses import dataclass, field
from uuid import uuid4

from . import entities, interfacies


@dataclass
class Users(interfacies.Users):
    storage: dict[str, entities.User] = field(default_factory=dict)

    def login(self, login: str, email: str) -> entities.User:
        user = self._login(email)
        if user:
            return user
        return self._register(login, email)

    def _login(self, email: str) -> entities.User | None:
        return self.storage.get(email)

    def _register(self, login: str, email: str) -> entities.User:
        primary_key = str(uuid4())
        user = entities.User(ident=primary_key, login=login, email=email)
        self.storage[user.ident] = user
        return user

    def get(self, ident: str) -> entities.User:
        return self.storage[ident]
