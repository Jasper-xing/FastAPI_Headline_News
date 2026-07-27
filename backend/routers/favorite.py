from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from crud import favorite
from schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse, FavoriteListResponse
from utils.response import success_response
from utils.auth import get_current_user
from starlette import status

router = APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")
async def check_favorite(
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user),
    news_id:int = Query(...,alias="newsId")
):
    result = await favorite.check_favorite(db,user.id,news_id)
    return success_response(msg="success",data=FavoriteCheckResponse(isFavorite=result))

@router.post("/add")
async def add_favorite(
    data:FavoriteAddRequest,
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    result = await favorite.add_favorite(db,user.id,data.news_id)
    return success_response(msg="收藏成功",data=result)

@router.delete("/remove")
async def delete_favorite(
    news_id:int = Query(...,alias="newsId"),
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    result = await favorite.delete_favorite(db,user.id,news_id)
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="未找到该收藏")
    return success_response(msg="取消收藏成功")

#查询收藏新闻列表
@router.get("/list")
async def get_favorite_list(
    page:int = Query(1,alias="page"),
    page_size:int = Query(10,alias="pageSize",le=100),
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    row,total = await favorite.get_favorite_list(db,user.id,page,page_size)
    hasmore = total > page * page_size
    favorite_list = [{
        **news.__dict__,
        "favoriteId":favorite_id,
        "favoriteTime":favorite_time
    }for news,favorite_time,favorite_id in row]
    data = FavoriteListResponse(list=favorite_list,total=total,has_more=hasmore)
    return success_response(msg="success",data=data)

#清空查询列表
@router.delete("/clear")
async def clear_favorite_list(
    db:AsyncSession = Depends(get_db),
    user:User = Depends(get_current_user)
):
    result = await favorite.clear_favorite_list(db,user.id)
    return success_response(msg=f"成功删除{result}条收藏")