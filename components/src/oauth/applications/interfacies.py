from abc import ABC, abstractmethod

from . import entities


class Users(ABC):

    @abstractmethod
    def login(self, login: str, email: str) -> entities.User:
        """Авторизация пользователя."""

    @abstractmethod
    def get(self, ident: str) -> entities.User:
        """Получение пользователя."""
