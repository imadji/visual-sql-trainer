from pydantic import BaseModel


class UserPD(BaseModel):
    login: str
    password: str


class SQLQuery(BaseModel):
    query: str
    user: str


class TaskSoltion(BaseModel):
    query: str
    user: str
    task_id: int
