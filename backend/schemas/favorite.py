from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase

class FavoriteCheckResponse(BaseModel):
    is_favorite: bool=Field(...,alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    news_id: int=Field(...,alias="newsId")

class Favoritelist(NewsItemBase):
    favorite_id: int=Field(alias="favoriteId")
    favorite_time: datetime=Field(alias="favoriteTime")
    
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名称填充数据
        from_attributes=True # 允许从ORM对象属性取值
    )

class FavoriteListResponse(BaseModel):
    list: list[Favoritelist]
    total: int=Field(alias="total")
    has_more: bool=Field(alias="hasMore")
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名称填充数据
        from_attributes=True # 允许从ORM对象属性取值
    )