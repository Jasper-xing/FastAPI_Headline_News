from fastapi import APIRouter, Depends, HTTPException, Query
from crud import news,news_cache
from config.db_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/api/news",tags=["news"])#创建APIRouter实例

#接口实现流程：
# 1.模块化路由-》API接口规范
# 2.定义模型类-》数据库表结构
# 3.在crud里面定义函数，封装操控数据库的方法
# 4.在路由处理模块调用crud方法

# 获取新闻分类列表思路：查询新闻分类即可
@router.get("/categories")
async def get_categories(db:AsyncSession=Depends(get_db),skip:int=0,limit:int=100):
    """
    获取新闻分类
    """
    categories = await news_cache.get_categories(db,skip,limit)

    return {
        "code":200,
        "message":"success",
        "data":categories
    }

#获取新闻列表思路：处理分页规则；查询新闻列表；获取总数；查看是否还有
@router.get("/list")
async def get_news_list(db:AsyncSession=Depends(get_db),
                        category_id:int=Query(...,alias="categoryId"),
                        page:int=1,
                        page_size:int=Query(default=10,le=100,alias="pageSize")):
    """
    获取新闻列表
    """
    skip = (page-1)*page_size
    news_list = await news_cache.get_news_list(db,category_id,skip,page_size)
    total = await news.get_news_count(db,category_id)
    hasMore = True if total > skip+page_size else False

    return {
        "code":200,
        "message":"success",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":hasMore
        }
    } 

#获取新闻详情思路：查询新闻详情+浏览量加一+推荐相关新闻
@router.get("/detail")
async def get_news_detail(db:AsyncSession=Depends(get_db),news_id:int=Query(...,alias="id")):
    news_detail = await news_cache.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")
    if not await news.increase_news_views(db,news_id):
        raise HTTPException(status_code=404,detail="更新浏览量失败")
    if isinstance(news_detail, dict):
        category_id = news_detail.get('categoryId') or news_detail.get('category_id')
        response_data = {
            "id": news_detail.get('id'),
            "title": news_detail.get('title'),
            "content": news_detail.get('content'),
            "image": news_detail.get('image'),
            "author": news_detail.get('author'),
            "publishTime": news_detail.get('publishTime'),
            "categoryId": news_detail.get('categoryId'),
            "views": news_detail.get('views'),
        }
    else:
        category_id = news_detail.category_id
        response_data = {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
        }
    
    related_news = await news_cache.get_related_news(db, news_id, category_id)
    response_data["relatedNews"] = related_news
    
    return {
        "code":200,
        "message":"success",
        "data": response_data
    }