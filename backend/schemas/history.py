from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.base import NewsItemBase


class NewsData(BaseModel):
    news_id: int=Field(...,alias="newsId")

class HistoryList(NewsItemBase):
    history_id: int=Field(alias="historyId")
    view_time: datetime=Field(alias="viewTime")
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名称填充数据
        from_attributes=True # 允许从ORM对象属性取值
    )

class HistoryListResponse(BaseModel):
    list:list[HistoryList]
    total: int=Field(alias="total")
    has_more: bool=Field(alias="hasMore")
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名称填充数据
        from_attributes=True # 允许从ORM对象属性取值
    )

