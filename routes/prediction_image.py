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


@router.get("/{type_test}/{type_point}")
async def prediction(type_point: str,type_test: str,token: str = Depends(get_token)):
    # print(type_prediction)
    # print(token)
    
    status_for_test = True
    data = None
    try:
        
        if(type_test=='yes'):
            status_for_test = True
        elif(type_test=='no'):
            status_for_test = False

        setup = PredictionImage(accessToken=token,type_point=type_point,status_test=status_for_test)
        data = setup.predictions()
    except Exception as e:
        # print(e)
        data = {"status":500,"message":'error can not prediction, check file core/prediction_image.py'}

    return data
