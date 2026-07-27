from fastapi import HTTPException
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.favorite import Favorite
from models.news import News

async def check_favorite(db:AsyncSession,user_id:int,news_id:int):
    query = select(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None

async def add_favorite(db:AsyncSession,user_id:int,news_id:int):
    if await check_favorite(db,user_id,news_id): 
        raise HTTPException(status_code=400,detail="已经收藏")
    news_favorite = Favorite(user_id=user_id,news_id=news_id)
    db.add(news_favorite)
    await db.commit()
    await db.refresh(news_favorite)
    return news_favorite
    
async def delete_favorite(db:AsyncSession,user_id:int,news_id:int):
    stmt = delete(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount>0

#查询收藏列表思路：db，用户id，分页参数，根据收藏表中的新闻id联合查询新闻表，从而获取新闻信息；因为要判断hasmore,所以需要查询的总数量
async def get_favorite_list(db:AsyncSession,user_id:int,page:int=1,page_size:int=10):
    offset = (page-1)*page_size
    stmt = select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id")).join(
        Favorite,News.id==Favorite.news_id).where(
        Favorite.user_id==user_id).order_by(Favorite.created_at.desc()
        ).offset(offset).limit(page_size)
    favorite_list = (await db.execute(stmt)).all()
    total = select(func.count(Favorite.id)).where(Favorite.user_id==user_id)
    total_count = (await db.execute(total)).scalar_one()
    return favorite_list,total_count

#清空收藏列表并返回清空的数量
async def clear_favorite_list(db:AsyncSession,user_id:int):
    # count = select(func.count(Favorite.id)).where(Favorite.user_id==user_id)
    # total_count = (await db.execute(count)).scalar_one()
    stmt = delete(Favorite).where(Favorite.user_id==user_id)
    result = await db.execute(stmt)
    total_count = result.rowcount or 0 #返回删除多少条记录
    await db.commit()
    return total_count
    