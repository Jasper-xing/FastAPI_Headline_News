from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    """
    ⽤户信息基础数据模型
    """

    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像UR")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True # 允许从ORM对象属性取值
    )
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse=Field(...,alias="userInfo")

    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名称填充数据
        from_attributes=True # 允许从ORM对象属性取值
    )

class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

class UserPasswordUpdateRequest(BaseModel):
    old_password: str=Field(...,alias="oldPassword")
    new_password: str=Field(...,alias="newPassword")
    model_config = ConfigDict(
        populate_by_name=True, # 通过字段名称填充数据
        from_attributes=True # 允许从ORM对象属性取值
    )