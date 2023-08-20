from typing import Union
import os
from fastapi import FastAPI, Request, Response, Depends, Header, HTTPException
from fastapi.security.http import HTTPBearer
from core.light import Light
from fastapi.middleware.cors import CORSMiddleware
from modules.test.test_main import Tests
from starlette import status
from pydantic import BaseModel
from fastapi.responses import FileResponse
from routes import smartbin,prediction_image,check_bin,set_light

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(smartbin.router)
app.include_router(prediction_image.router)
app.include_router(check_bin.router)
app.include_router(set_light.router)


@app.get("/")
async def read_root(request: Request, response: Response):
    # print(request.query_params.get("open"))
    try:
        
        if ('Bearer '+os.getenv('KEY_APP') == request.headers['authorization']):
            response.status_code = 200
            return {"satus": 'good'}
        else:
            response.status_code = 404
            return {"satus": 'token not find or type token not find'}
    except:
        response.status_code = 404
        return {"satus": 'token not find or type token not find'}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8080,
                reload=True, env_file='.env.dev')
