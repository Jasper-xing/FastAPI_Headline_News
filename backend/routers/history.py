from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.history import HistoryListResponse, NewsData
from config.db_conf import get_db
from crud import history
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from starlette import status

router = APIRouter(prefix="/api/history",tags=["history"])

@router.post("/add")
async def add_history(
    newsid:NewsData,
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    data=await history.add_history(db,user.id,newsid.news_id)
    return success_response(msg="添加成功",data=data)

#获取浏览历史列表
@router.get("/list")
async def get_history_list(
    page:int=Query(1,alias="page"),
    page_size:int=Query(10,alias="pageSize",le=100),
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    row,total = await history.get_history_list(db,user.id,page,page_size)
    history_list = [{
        **news.__dict__,
        "viewTime":view_time,
        "historyId":history_id
    }for news,view_time,history_id in row]
    hasmore = total > page * page_size
    data = HistoryListResponse(list=history_list,total=total,has_more=hasmore)
    return success_response(msg="获取成功",data=data)

@router.delete("/delete/{history_id}")
async def delete_history(
    history_id:int,
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    result = await history.delete_history(db,user.id,history_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="未找到该浏览历史")
    return success_response(msg="删除成功")

@router.delete("/clear")
async def clear_history(
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    result = await history.clear_history(db,user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="未找到浏览历史")
    return success_response(msg="清空成功")