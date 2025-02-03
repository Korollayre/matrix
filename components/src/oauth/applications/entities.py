from dataclasses import dataclass


@dataclass
class User:
    ident: str
    email: str
    login: str
