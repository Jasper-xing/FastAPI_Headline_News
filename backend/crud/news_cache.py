from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from cache.news_cache import get_cache_news_detail, get_cache_news_list, get_cache_related_news, get_categories_cache, set_cache_news_detail, set_cache_news_list, set_cache_related_news, set_categories_cache

# 获取新闻分类
async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    #如果有缓存先读缓存里的
    cached_categories =await get_categories_cache()
    if cached_categories:
        return cached_categories
    
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    #写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_categories_cache(categories)
    return categories


# 获取新闻列表
async def get_news_list(db:AsyncSession,
                        category_id:int,
                        skip:int=0,
                        page_size:int=10):
    page = skip//page_size+1
    cached_list = await get_cache_news_list(category_id,page,page_size)
    if cached_list:
        return cached_list
    
    stmt = select(News).where(News.category_id==category_id).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    news_list = result.scalars().all()
   
    if news_list:
        news_list = jsonable_encoder(news_list)
        await set_cache_news_list(category_id,page,page_size,news_list)
    return news_list

# 获取相关新闻类总数量
async def get_news_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id==category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

# 获取新闻详情
async def get_news_detail(db:AsyncSession,news_id:int):
    cached_news_detail = await get_cache_news_detail(news_id)
    if cached_news_detail:
        return cached_news_detail

    stmt = select(News).where(News.id==news_id)
    result = await db.execute(stmt)
    news_detail = result.scalar_one_or_none()
    if news_detail:
        news_detail = jsonable_encoder(news_detail)
        await set_cache_news_detail(news_id,news_detail)
    return news_detail


#更新浏览量
async def increase_news_views(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id==news_id).values(views=News.views+1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount>0

#获取相关新闻推荐
async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int=5):
    cached_related_news = await get_cache_related_news(news_id,category_id,limit)
    if cached_related_news:
        return cached_related_news
    
    stmt = select(News).where(
        News.id!=news_id,
        News.category_id==category_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    
    related_news_list = [{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time.isoformat() if news_detail.publish_time else None,
            "categoryId":news_detail.category_id,
            "views":news_detail.views
    }for news_detail in related_news]
    if related_news_list:
        await set_cache_related_news(news_id,category_id,related_news_list,limit)
    return related_news_list
    