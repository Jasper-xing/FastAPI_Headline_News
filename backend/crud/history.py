from datetime import datetime

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News

async def add_history(db:AsyncSession,user_id:int,news_id:int):
    #查询是否已经存在，存在就更新浏览时间
    stmt = select(History).where(History.user_id==user_id,History.news_id==news_id)
    result = (await db.execute(stmt)).scalar_one_or_none()
    if result:
        updated_history = update(History).where(History.user_id==user_id,History.news_id==news_id).values(view_time=datetime.now())
        await db.execute(updated_history)
        await db.commit()
        await db.refresh(result)
        return result
    news_history = History(user_id=user_id,news_id=news_id)
    db.add(news_history)
    await db.commit()
    await db.refresh(news_history)
    return news_history

async def get_history_list(db:AsyncSession,user_id:int,page:int,page_size:int):
    count = select(func.count(History.id)).where(History.user_id==user_id)
    total = (await db.execute(count)).scalar_one()
    offset = (page-1)*page_size
    stmt = select(News,History.view_time,History.id.label("history_id")).join(
        History,History.news_id==News.id).where(
        History.user_id==user_id).order_by(
        History.view_time.desc()).offset(offset).limit(page_size)
    history_list = (await db.execute(stmt)).all()
    return history_list,total

async def delete_history(db:AsyncSession,user_id:int,history_id:int):
    stmt = delete(History).where(History.id==history_id,History.user_id==user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount>0

async def clear_history(db:AsyncSession,user_id:int):
    stmt = delete(History).where(History.user_id==user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount>0