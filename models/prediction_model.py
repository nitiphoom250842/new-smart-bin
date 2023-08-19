from pydantic import BaseModel


class PredictionModel(BaseModel):
    image_path: str
    access_token: str
