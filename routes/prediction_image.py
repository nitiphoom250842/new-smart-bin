# routes\prediction_image.py
from fastapi import Depends,  HTTPException, APIRouter, Request
from fastapi.security.http import HTTPBearer
from starlette import status
from pydantic import BaseModel
import os
from core.prediction_image import PredictionImage



router = APIRouter(
    prefix='/api/v1/smartbin/prediction',
    tags=['Smart Bin v1'],
    responses={
        404: {
            'message': 'Not Found'
        }
    }
)

get_bearer_token = HTTPBearer()


class UnauthorizedMessage(BaseModel):
    detail: str = "Unauthorized"


async def get_token(request: Request,tok: str = Depends(get_bearer_token)) -> str:
    try:
        # print(request.headers[os.getenv('HEADERS_NAME')])
        if os.getenv('HEADERS_VALUE') == request.headers[os.getenv('HEADERS_NAME')]:
            return tok.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=UnauthorizedMessage().detail,
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedMessage().detail,
        )


@router.get("/{type_point}")
async def prediction(type_point: str,token: str = Depends(get_token)):
    # print(type_prediction)
    # print(token)
    data = PredictionImage(AccessToken=token,type_point=type_point)
    data.predictions()
    return {
        'wine': 80,
        'plastic': 20,
        'can': 100,
    }
