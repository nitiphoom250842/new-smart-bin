from fastapi import Depends,  HTTPException, APIRouter, Request
from fastapi.security.http import HTTPBearer
from starlette import status
from pydantic import BaseModel
import os
from core.bin_details import BinDetails



router = APIRouter(
    prefix='/api/v1/smartbin/check-bin',
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


@router.get("/{type_test}")
async def get_details_bin(type_test: str,token: str = Depends(get_token)):
    return {
        'wine': 80,
        'plastic': 20,
        'can': 100,
    }
