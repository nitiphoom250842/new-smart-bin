from pydantic import BaseModel


class AccessTokenModel(BaseModel):
    access_token: str
