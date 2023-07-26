from typing import Union
import os
from fastapi import FastAPI, Request, Response
from core.light import Light
from fastapi.middleware.cors import CORSMiddleware
from modules.test.test_main import Tests


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
async def read_root(request:Request,response: Response):
    # print(request.query_params.get("open"))
    if('Bearer '+os.getenv('KEY_APP')==request.headers['authorization']):
        response.status_code = 200
        return {"satus": 'good'}
    else:
        response.status_code = 404
        return {"satus": 'token not find or type token not find'}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

