from datetime import datetime, timedelta
import uuid

from fastapi import HTTPException

from models.users import User, UserToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from utils import security
from schemas.users import UserRequest


#根据用户名去查询数据库，如果存在则返回用户信息，不存在则返回错误信息
async def get_user_by_username(db:AsyncSession,username:str) :
    stmt = select(User).where(User.username==username)
    user = await db.execute(stmt)
    return user.scalar_one_or_none()

#创建用户,使用哈希加密密码
async def create_user(db:AsyncSession,user_data:UserRequest) :
    hashed_password = security.get_hash_password(user_data.password)
    new_user = User(username=user_data.username,password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

#生成token：创建token，设置到期时间，查寻UserToken表中是否有user_id的token，有则更新，无则创建
async def create_user_token(db:AsyncSession,user_id:int):
    token = str(uuid.uuid4())
    expires_time = datetime.now() + timedelta(days=7)
    stmt = select(UserToken).where(UserToken.user_id==user_id)
    query = await db.execute(stmt)
    result = query.scalar_one_or_none()
    if result:
        result.token = token
        result.expires_at = expires_time
        target_obj = result
    
    else:
        new_token = UserToken(user_id=user_id,token=token,expires_at=expires_time)
        db.add(new_token)
        target_obj = new_token
    await db.commit()
    await db.refresh(target_obj)
    return token

#验证用户是否存在
async def authenticate_user(db:AsyncSession,username:str,password:str) :
    user = await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None
    return user

#token：根据token查询用户详情
async def get_user_by_token(db:AsyncSession,token:str) :
    stmt = select(UserToken).where(UserToken.token==token)
    query = await db.execute(stmt)
    result = query.scalar_one_or_none()
    if not result or result.expires_at < datetime.now():#查不到或者令牌过期
        return None
    stmt = select(User).where(User.id==result.user_id)
    query = await db.execute(stmt)
    return query.scalar_one_or_none()

#更新用户信息，之前写了一个根据用户名查询用户信息，这里复用
async def update_user(db:AsyncSession,username:str,user_data:UserRequest) :
    user = await get_user_by_username(db,username)
    if not user:
        return None
    stmt = update(User).where(User.username==username).values(**user_data.model_dump(
        exclude_unset=True,#忽略未设置属性
        exclude_none=True
    ))
    result = await db.execute(stmt)
    await db.commit()
    #检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="用户不存在")
    updated_user = await get_user_by_username(db,username)
    return updated_user

#修改用户密码，使用哈希加密
async def update_user_password(db:AsyncSession,user:User,old_password:str,new_password:str) :
    if not security.verify_password(old_password,user.password):
        return False
    new_password_hash = security.get_hash_password(new_password)
    user.password = new_password_hash
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True
