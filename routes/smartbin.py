import json
import os
from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.security.http import HTTPBearer
from starlette import status
from pydantic import BaseModel
from fastapi.responses import FileResponse
import mimetypes

from core.base_service import BaseService
from core.custom_error import bad_request, not_found, unauthorized
from models.prediction_model import PredictionModel
from models.user_select_type_model import UserSelectType


save_login_qrcode_path = os.path.join(
    os.getcwd(), "assets", "images", "login_qr_code.png"
)

router = APIRouter(
    prefix="/api/v1/smartbin",
    tags=["Smart Bin v1"],
    responses={404: {"message": "Not Found"}},
)

get_bearer_token = HTTPBearer()

apiSuccessList = [True, False]


class UnauthorizedMessage(BaseModel):
    detail: str = "Unauthorized"


async def get_token(tok: str = Depends(get_bearer_token)) -> str:
    try:
        if tok.scheme == "Bearer" and tok.credentials == os.getenv("KEY_APP"):
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


base_service = BaseService()


@router.get("/amount_waste")
async def amount_waste(request: Request, _: str = Depends(get_token)):
    print(request.base_url)
    print(request.headers)
    print(request.method)
    return {"can": 80.0, "plastic": 20.0, "pet": 100.0, "trash": 30.0}


@router.get("/get_data_type")
def get_data_type(_: str = Depends(get_token)):
    url = "/v1/bin/secret/types"

    try:
        res = base_service.get(url)
        return json.loads(res.text)
    except:
        raise bad_request(http_method="POST")


@router.put("/update_capacity_bin")
async def update_capacity_bin(
    can: int, pet: int, plastic: int, unknown: int, _: str = Depends(get_token)
):
    url = "/v1/bin/secret/quantities"
    json_data = {"data": f"0:{can}/1:{pet}/2:{plastic}/3:{unknown}"}

    try:
        res = base_service.post(url, json=json_data)
        return json.loads(res.text)
    except:
        raise bad_request(http_method="POST")


@router.post("/bin_report_error")
def bin_report_error(_: str = Depends(get_token)):
    url = "/v1/bin/secret/status"

    """
    code
        - 1   ถังขยะเต็ม
        - 3   ถังขยะเสีย

    message
        - ถังขยะเต็มเฉพาะถังที่ 1
        - ไม่สามารถเชื่อมต่อกล้องได้
    """

    json_data = {"code": 1, "message": "ถังขยะเต็มเฉพาะถังที่ 1"}

    try:
        res = base_service.post(url, json=json_data)
        return json.loads(res.text)
    except:
        raise bad_request(http_method="POST")


@router.post("/login_student_id")
async def login_student_id(student_id, _: str = Depends(get_token)):
    url = "/v1//bin/secret/login/uname"
    # 6340202784
    # 6440202254

    try:
        res = base_service.post(
            url=url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"uname": f"b{student_id}"},
        )

        if res.status_code == 404:
            raise not_found(http_method="POST")

        return json.loads(res.text)

        # if 'access_token' in res.text:
        #     access_token = json.loads(res.text)['access_token']
        #     return access_token
    except:
        raise bad_request(http_method="POST")


@router.get("/login_qrcode")
async def login_qrcode():
    url = "/v1/bin/secret/login/qrcode"

    try:
        res = base_service.get(url)

        fp = open(save_login_qrcode_path, "wb")
        fp.write(res.content)
        fp.close()

        return FileResponse(save_login_qrcode_path)
    except:
        raise not_found(http_method="GET")


@router.get("/get_qrcode_access_token")
async def get_qrcode_access_token(_: str = Depends(get_token)):
    url = "/v1/bin/secret/login/check"

    try:
        res = base_service.get(url)

        if res.status_code == 401:
            raise unauthorized(http_method="GET")

        return json.loads(res.text)
    except:
        raise bad_request(http_method="GET")


@router.post("/user_select_type")
def user_select_type(items: UserSelectType, _: str = Depends(get_token)):
    print(items.type)
    print(items.user)
    print(items.datetime)
    return {"message": items}


@router.post("/prediction_login")
def prediction_login(items: PredictionModel, _: str = Depends(get_token)):
    url = "/prediction/"
    headers = {"Authorization": f"Bearer {items.access_token}", "Content-Type": None}

    image_name = os.path.basename(items.image_path)
    image_type = mimetypes.guess_type(image_name)[0]
    files = {"image": (image_name, open(items.image_path, "rb"), image_type)}

    try:
        res = base_service.postImage(
            url,
            files=files,
            headers=headers,
        )
        return json.loads(res.text)
    except:
        raise bad_request(http_method="POST")


@router.post("/prediction_donate")
def prediction_donate(items: PredictionModel, _: str = Depends(get_token)):
    print(items.image_path)
    print(items.access_token)
    url = "/prediction/?mode=donate"
    # image_path = 'assets/images/plastic.jpg'

    try:
        image_name = os.path.basename(items.image_path)
        image_type = mimetypes.guess_type(image_name)[0]

        headers = {"Content-Type": None}
        files = {"image": (image_name, open(items.image_path, "rb"), image_type)}

        res = base_service.postImage(
            url,
            files=files,
            headers=headers,
        )
        return json.loads(res.text)
    except:
        raise bad_request(http_method="GET")
