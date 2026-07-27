from fastapi import Depends, HTTPException, Header
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from crud.users import get_user_by_token
#根据令牌查询用户信息，返回用户
async def get_current_user(
        db:AsyncSession = Depends(get_db),
        authorization:str = Header(...,alias="Authorization")
) :
    token = authorization.replace("Bearer ","")
    user = await get_user_by_token(db,token)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效令牌")
    return user
