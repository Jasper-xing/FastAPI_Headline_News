from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserAuthResponse, UserInfoResponse, UserPasswordUpdateRequest, UserRequest, UserUpdateRequest
from crud import users
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
router = APIRouter(prefix="/api/user",tags=["users"])

#用户注册思路：1.用户输入用户名进入请求，2.验证用户名是否已存在，3.创建用户，4生成访问令牌，5.响应请求
@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    if await users.get_user_by_username(db,user_data.username): #判断用户名是否已存在
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户名已存在")
    new_user = await users.create_user(db,user_data)
    new_user.token = await users.create_user_token(db,new_user.id)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": new_user.token,
    #         "userInfo": {
    #         "id": new_user.id,
    #         "username": new_user.username,
    #         "bio": new_user.bio,
    #         "avatar": new_user.avatar
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=new_user.token,user_info=UserInfoResponse.model_validate(new_user))
    return success_response(msg="注册成功",data=response_data)

#用户登录思路：1.用户输入用户名和密码进入请求，2.验证用户名是否已存在，3.验证密码，4生成访问令牌，5.响应请求
@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user: #验证用户和密码
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token = await users.create_user_token(db,user.id)
    response_data = UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(msg="登录成功",data=response_data)

#用户信息查询思路：1.校验token，2.封装工具函数，之后查询用户令牌时要用，3.查询信息，4.路由导入：依赖注入
@router.get("/info")
async def get_user_info(user:User=Depends(get_current_user)):
    return success_response(msg="获取用户信息成功",data=UserInfoResponse.model_validate(user) )

#修改用户信息思路：1.校验token，2.更新（用户输入数据，put提交；请求头参数；定义pydantic模型类），3.响应结果
#参数：1.用户输入数据，2.token验证的，3.db（需要执行更新操作）
@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    user = await users.update_user(db,user.username,user_data)
    return success_response(msg="修改用户信息成功",data=UserInfoResponse.model_validate(user))

#改密码思路：1.校验token，2.核验旧密码，3.验证密码
@router.put("/password")
async def update_password(user_data:UserPasswordUpdateRequest,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    if not await users.update_user_password(db,user,user_data.old_password,user_data.new_password):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="旧密码错误，请重新输入")
    return success_response(msg="修改密码成功",data=UserInfoResponse.model_validate(user))
