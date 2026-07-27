from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

# 获取新闻分类
async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

# 获取新闻列表
async def get_news_list(db:AsyncSession,
                        category_id:int,
                        skip:int=0,
                        page_size:int=10):
    stmt = select(News).where(News.category_id==category_id).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    return result.scalars().all()

# 获取相关新闻类总数量
async def get_news_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id==category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

# 获取新闻详情
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id==news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#更新浏览量
async def increase_news_views(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id==news_id).values(views=News.views+1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount>0

#获取相关新闻推荐
async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int=5):
    stmt = select(News).where(
        News.id!=news_id,
        News.category_id==category_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    return [{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views
    }for news_detail in related_news]