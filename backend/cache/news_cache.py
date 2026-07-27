from typing import Any, Dict, List, Optional

from config.cache_conf import get_json_cache, set_cache


CATEGORIES_KEY = "news:categories"
NEWS_LIST_PRIFIX = "news_list:"
async def get_categories_cache():
    """获取新闻分类缓存"""
    return await get_json_cache(CATEGORIES_KEY)

async def set_categories_cache(data:list[dict[str,Any]],expire:int=7200):
    """设置新闻分类缓存"""
    return await set_cache(CATEGORIES_KEY,data,expire)

async def set_cache_news_list(category_id:Optional[int],page:int,size:int,news_list:List[Dict[str,Any]],expire:int=1800):
    """设置新闻列表缓存"""
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PRIFIX}{category_part}:{page}{size}"
    return await set_cache(key,news_list,expire)

async def get_cache_news_list(category_id:Optional[int],page:int,size:int):
    """获取新闻列表缓存"""
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PRIFIX}{category_part}:{page}{size}"
    return await get_json_cache(key)

async def get_cache_news_detail(news_id:int):
    """获取新闻详情缓存"""
    key = f"news:{news_id}"
    return await get_json_cache(key)

async def set_cache_news_detail(news_id:int,news_detail:Dict[str,Any],expire:int=1800):
    """设置新闻详情缓存"""
    key = f"news:{news_id}"
    return await set_cache(key,news_detail,expire)

async def get_cache_related_news(news_id:int,category_id:int,limit:int=5):
    """获取相关新闻缓存"""
    key = f"news:{news_id}:{category_id}:{limit}"
    return await get_json_cache(key)

async def set_cache_related_news(news_id:int,category_id:int,related_news:List[Dict[str,Any]],limit:int=5,expire:int=1800):
    """设置相关新闻缓存"""
    key = f"news:{news_id}:{category_id}:{limit}"
    return await set_cache(key,related_news,expire)
