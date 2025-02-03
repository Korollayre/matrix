from pydantic import BaseModel


class OnGetCallback(BaseModel):
    state: str
    code: str
