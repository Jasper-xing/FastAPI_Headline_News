from fastapi import FastAPI
from routers import news,users,favorite,history
from fastapi.middleware.cors import CORSMiddleware

from utils.exception_handles import register_exception_handles

app = FastAPI()

register_exception_handles(app)
#可访问的域名
origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,#开发环境中可以写为*，实际中应写为与nodejs服务端同域的
    allow_credentials=True,#允许cookie
    allow_methods=["*"],#允许请求所有方法
    allow_headers=["*"],#允许所有请求头
)

app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)