from pydantic import BaseModel


class UserPD(BaseModel):
    login: str
    password: str
