from fastapi import Depends,  HTTPException, APIRouter
from fastapi.security.http import HTTPBearer
from starlette import status
from pydantic import BaseModel
from fastapi.responses import FileResponse


router = APIRouter(
    prefix='/api/v1/smartbin',
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


async def get_token(tok: str = Depends(get_bearer_token)) -> str:
    try:
        if tok.scheme == 'Bearer' and tok.credentials == '1234':
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


@router.get("/amount_waste")
async def amount_waste(token: str = Depends(get_token)):
    return {
        'wine': 80,
        'plastic': 20,
        'can': 100,
    }


@router.get("/login_qrcode")
async def login_qrcode(token: str = Depends(get_token)):
    return FileResponse("assets/images/qr-code.png")
