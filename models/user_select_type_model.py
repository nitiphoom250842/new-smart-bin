from pydantic import BaseModel


class UserSelectType(BaseModel):
    user: str
    type: str
    datetime: str
