import json
import os

import redis.asyncio as redis

# Redis 连接信息走环境变量，保留本地开发默认值（password 默认 None 表示无密码）
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

#创建 Redis 连接对象
redis_client = redis.Redis(
    host=REDIS_HOST, # Redis 服务器地址
    port=REDIS_PORT, # Redis 端口号
    db=REDIS_DB, # Redis 数据库编号
    password=REDIS_PASSWORD, # Redis 密码（默认无）
    decode_responses=True, # 自动将字节对象解码为字符串
    protocol=2
)

#设置和读取(字符串 列表或字典)
#读取字符串
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None    
#读取列表或字典
async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data) #序列化
        return None
    except Exception as e:
        print(f"获取 json 缓存失败：{e}")
        return None
#设置
async def set_cache(key:str,value:str,expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            #序列化转成字符串
            value = json.dumps(value,ensure_ascii=False,default=str)#确保中文正常
            await redis_client.setex(key,expire,value)
            return True
    except Exception as e:
        print(f"设置缓存失败：{e}")
        return False
        