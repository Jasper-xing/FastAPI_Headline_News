
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(msg:str="success",data=None):
    content = {
        "code": 200,
        "message": msg,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(content))