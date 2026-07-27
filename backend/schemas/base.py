from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str]=None
    image:Optional[str]=None
    author: Optional[str]=None
    category_id: int=Field(alias="categoryId")
    views:int
    publish_time: Optional[datetime]=Field(None,alias="publishedTime")

    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名称填充数据
        from_attributes=True # 允许从ORM对象属性取值
    )