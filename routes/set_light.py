from fastapi import Depends,  HTTPException, APIRouter, Request
from fastapi.security.http import HTTPBearer
from starlette import status
from pydantic import BaseModel
import os
from core.light import Light



router = APIRouter(
    prefix='/api/v1/smartbin/set-ligth',
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


@router.get("/{type_test}/{type_light}")
async def setup_light(type_light: str,type_test: str,token: str = Depends(get_token)):
    status_light = False
    status_for_test = True
    data = None
    try:
        if(type_test=='yes'):
            status_for_test = True
        elif(type_test=='no'):
            status_for_test = False

        if(type_light=='on'):
            status_light = True
        elif(type_light=='off'):
            status_light = False
        setup = Light(status_light= status_light,status_test=status_for_test)
        data = setup.setLight()
    except:
        data = {"status":500,"message":'error can not open light, check file core/light.py'}

    return data
