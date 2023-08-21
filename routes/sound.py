

import os
from threading import Thread
from fastapi import APIRouter, HTTPException
from starlette import status
import pygame

from core.custom_error import generate_common_header_response


router = APIRouter(
    prefix='/api/v1/sound',
    tags=['Sound Management'],
    responses={
        404: {
            'message': 'Not Found'
        }
    }
)


sound_data = {
    'main.start': '1-เริ่มใช้งาน.wav',
    'main.exchange': '2-แลกขยะ.wav',
    'main.howto': '3-วิธีใช้.wav',
    'all.back': '4-ย้อนกลับ.wav',
    'list.collect': '5-สะสมแต้ม.wav',
    'list.donate': '6-บริจาค.wav',
    'login.qrcode': '7-scan-QR-Code.wav',
    'login.sid': '8-ป้อนรหัสนิสิต.wav',
    'login.delete': '9-ลบ.wav',
    'all.enter': '10-ตกลง.wav',
    'all.back': '11-แลกเพิ่ม.wav',
    'all.back': '12-ดูคะแนน.wav',
    'all.back': '13-พร้อมทำงาน.wav',
    'all.back': '14-กำลังประมวลผล.wav',
    'all.back': '15-คะแนนสะสมครั้งนี้.wav',
    'all.back': '16-ยืนยัน.wav',
    'all.back': '17-ขอบคุณค่ะ.wav',
}


@router.get("/play")
async def play(command: str):
    try:
        sound_path = sound_data[command]
        play_sound(join_path(sound_path))

        return HTTPException(
            status_code=status.HTTP_200_OK,
            headers=generate_common_header_response('GET'),
        )
    except:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers=generate_common_header_response('GET'),
        )


def join_path(des: str) -> str:
    return os.path.join(
        os.getcwd(), 'assets', 'sound', des)


def play_sound(file):
    p = Thread(target=start_sound, args=(file,))
    p.start()


def start_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True:
        continue
