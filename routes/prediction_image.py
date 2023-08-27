# routes\prediction_image.py
from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.security.http import HTTPBearer
from starlette import status
from pydantic import BaseModel
import os
from core.custom_exception import APIPredictionError, CameraError, DoorError, DoorTimeout, MotorError, RemoveImageError
from core.prediction_image import PredictionImage
from models.access_token_model import AccessTokenModel


router = APIRouter(
    prefix="/api/v1/smartbin/prediction",
    tags=["Smart Bin v1"],
    responses={404: {"message": "Not Found"}},
)

get_bearer_token = HTTPBearer()


class UnauthorizedMessage(BaseModel):
    detail: str = "Unauthorized"


async def get_token(request: Request, tok: str = Depends(get_bearer_token)) -> str:
    try:
        # print(request.headers[os.getenv('HEADERS_NAME')])
        if (
            "Bearer " + os.getenv("HEADERS_VALUE")
            == request.headers[os.getenv("HEADERS_NAME")]
        ):
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


@router.post("/{type_test}/{type_point}")
async def prediction(
    items: AccessTokenModel,
    type_point: str,
    type_test: str,
    _: str = Depends(get_token),
):
    status_for_test = True

    try:
        if type_test == "yes":
            status_for_test = True

        elif type_test == "no":
            status_for_test = False

        setup = PredictionImage(
            accessToken=items.access_token,
            type_point=type_point,
            status_test=status_for_test,
        )

        return setup.predictions()
    
    except DoorTimeout:
        raise HTTPException(status_code=502, detail="door timeout")

    except DoorError:
        raise HTTPException(status_code=503, detail="door error")

    except CameraError:
        raise HTTPException(status_code=503, detail="camera error")

    except APIPredictionError:
        raise HTTPException(status_code=503, detail="api prediction error")

    except MotorError:
        raise HTTPException(status_code=503, detail="motor error")

    except RemoveImageError:
        raise HTTPException(status_code=503, detail="remove image error")
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="error can not prediction, check file core/prediction_image.py",
        )
