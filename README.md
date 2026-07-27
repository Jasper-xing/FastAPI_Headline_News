# Headline_News_Backend

这是一个基于FastAPI开发的新闻后端系统,主要功能包括新闻分类管理、新闻列表、新闻分页查询、用户收藏和浏览历史等。采用前后端分离架构。

## 技术栈

| 类别 | 技术 |
| --- | --- |
| Web 框架 | FastAPI |
| 数据库 | MySQL + SQLAlchemy 2.0（异步） |
| 缓存 | Redis（异步） |
| 数据校验 | Pydantic v2 |
| 异步驱动 | aiomysql + redis.asyncio |

## 项目结构：

FastAPI_news_backend/

├── main.py \# FastAPI 应用入口。创建 app、配置 CORS(仅放行 localhost:5173)、注册全局异常处理器、挂载 4 个路由,本地 uvicorn 监听 8000 端口

├── requirements.txt \# 依赖清单(FastAPI、SQLAlchemy、aiomysql、redis、pydantic、bcrypt、uvicorn 等)

├── test_main.http \# REST Client 风格的接口测试脚本,可直接在 IDE 里发请求调试

├── .vscode/

│ └── settings.json \# VSCode 工作区配置(非业务代码)

│

├── config/ \# 配置层

│ ├── \_\_init\_\_.py \# 包标识(空)

│ ├── db_conf.py \# 异步 MySQL 引擎配置 + get_db 依赖注入(会话自动提交/回滚/关闭)

│ └── cache_conf.py \# 异步 Redis 客户端 + 通用缓存读写函数(get_cache/get_json_cache/set_cache)

│

├── models/ \# ORM 模型层

│ ├── \_\_init\_\_.py \# 包标识(空)

│ ├── news.py \# News(新闻表)、Category(分类表)模型,自带公共 created_at/updated_at 字段

│ ├── users.py \# User(用户表)、UserToken(令牌表)模型(注意:这里的 Base 没有继承公共时间字段)

│ ├── favorite.py \# Favorite(收藏表)模型

│ └── history.py \# History(浏览历史表)模型

│

├── schemas/ \# Pydantic 校验层

│ ├── \_\_init\_\_.py \# 包标识(空)

│ ├── base.py \# 公共基础模型 NewsItemBase(统一 from_attributes、别名映射等配置)

│ ├── users.py \# 用户相关请求/响应模型(注册、登录、信息更新、改密码)

│ ├── favorite.py \# 收藏相关模型

│ └── history.py \# 浏览历史相关模型

│

├── crud/ \# 数据访问层

│ ├── \_\_init\_\_.py \# 包标识(空)

│ ├── news.py \# 新闻基础数据库操作(列表/详情/计数/相关推荐/浏览量+1),不含缓存

│ ├── news_cache.py \# 带缓存优先逻辑的版本(分类/列表/详情/相关推荐),路由实际调用它

│ ├── users.py \# 用户 CRUD + 令牌生成/校验

│ ├── favorite.py \# 收藏的增删查/清空

│ └── history.py \# 浏览历史的记录/查询/删除/清空

│

├── routers/ \# 路由层(对外 API)

│ ├── \_\_init\_\_.py \# 包标识(空)

│ ├── news.py \# 新闻接口: /api/news/categories、/list、/detail

│ ├── users.py \# 用户接口: /api/user/register、/login、/info、/update、/password

│ ├── favorite.py \# 收藏接口(增/删/列表/清空)

│ └── history.py \# 历史记录接口(记录/列表/删除/清空)

│

├── cache/ \# 缓存键管理层

│ └── news_cache.py \# 仅封装缓存键名生成与读写(分类/列表/详情/相关推荐),不含业务逻辑

│

└── utils/ \# 公共工具层

├── \_\_init\_\_.py \# 包标识(空)

├── auth.py \# get_current_user 鉴权依赖,从 Authorization: Bearer 头取 token 校验用户

├── security.py \# bcrypt 密码哈希与校验(get_hash_password / verify_password)

├── response.py \# 统一响应格式 success_response → {code, message, data}

├── exception.py \# 分级异常处理器实现(HTTP / 数据完整性 / SQLAlchemy / 通用兜底)

└── exception_handles.py \# 把上面的处理器注册到 app(被 main.py 调用)

## 环境准备：

1.安装Anaconda23.10 ~ 23.11.x或25.x，创建fastapi_env环境：

`conda create -n fastapi_env python=3.12 -y`

激活fastapi_env环境：

conda activate fastapi_env

2.下载相应的三方库：

直接复制到终端下载（注意终端前面显示 (fastapi_env)）

`pip install aiomysql==0.3.2 annotated-types==0.7.0 anyio==4.13.0 bcrypt==4.0.1 cffi==2.0.0 click==8.3.3 colorama==0.4.6 cryptography==48.0.0 fastapi==0.115.12 greenlet==3.5.0 h11==0.16.0 idna==3.15 packaging==26.0 passlib==1.7.4 pycparser==3.0 pydantic==2.13.4 pydantic_core==2.46.4 PyMySQL==1.2.0 redis==8.0.0 setuptools==82.0.1 SQLAlchemy==2.0.49 starlette==0.46.2 typing-inspection==0.4.2 typing_extensions==4.15.0 uvicorn==0.34.2 wheel==0.46.3`

或者执行

`pip install -r requirements.txt`

下载慢的话挂梯子或添加镜像源

`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

3.安装MySQL：

本地安装MySQL8.0.x，确保加入环境变量，打开cmd（管理员），启动MySQL

`net start mysql_news`

进入mysql\>交互端

`.\mysql -u root -p`

创建数据库

`CREATE DATABASE IF NOT EXISTS news_app DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

退出交互端

`exit`

执行

`.\mysql -u root -p news_app < "换成自己的sql路径"`（注意这是在cmd下执行）

Vscode上安装database插件，连接服务，填主机名、端口、用户名和密码，将数据库连接至vscode，可以查看sql中的表

注意：我的数据库名：news_app， MySQL服务名：mysql_news

4.安装Redis

本地安装Redis，默认端口是6379，启动Redis

`redis-server.exe redis.windows.conf`（Redis目录下执行）

5.环境配置

Mysql 和 Redis 的连接信息通过环境变量配置（详见下方「安全提示」），并已保留本地开发默认值，一般无需修改即可直接运行：

- 复制仓库根目录的 `.env.example` 为 `.env`（可选），按需覆盖以下变量：
  - MySQL：`DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` / `DB_NAME`
  - Redis：`REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` / `REDIS_PASSWORD`
- 默认值即 `root` / `123456` / `localhost` / `3306` / `news_app`（MySQL）与 `localhost` / `6379` / `0`（Redis），本地可直接使用。
- 也可在 `config/db_conf.py` 与 `config/cache_conf.py` 中查看/修改这些默认值。

## 启动项目：

1.确保是在fastapi_env环境下：

`python main.py`

启动成功：

`INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`

`INFO: Started reloader process [13920] using StatReload`

`INFO: Started server process [6740]`

`INFO: Waiting for application startup.`

`INFO: Application startup complete.`

2.打开浏览器输入：

[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

进入**Swagger UI**，可以测试每个接口，包括news、users、favorite、history四个部分组成（附录有api接口总览）

3.打开cmd启动前端界面：

`npm run dev`(要在“你自己的路径\frontend\xwzx-news”下)

打开浏览器输入：

[`http://localhost:5173/`](http://localhost:5173/)

（由于之前MySQL和Redis都启动过，所以上述操作没重复了，接下来演示完整启动流程：

1.启动MySQL（管理员权限下的cmd）：

`net start mysql_news`

2.启动Redis（cmd，要在Redis目录下）：

`redis-server.exe redis.windows.conf`

3.启动前端（cmd，要在前端目录下）：

`npm run dev`

4.启动后端（cmd，要在后端目录下）：

`python main.py`

5.Headline_News项目启动完成，访问：

[`http://localhost:5173/`](http://localhost:5173/)

）

## 仓库未包含的内容与补回方法

本仓库**只提交源码**，整体体积仅几百 KB。本地运行所需的数据库、缓存、运行时等二进制与依赖**没有放进 git**，原因统一为：体积过大（如 MySQL 安装目录约 1.1 GB）、跨平台不兼容（多为 Windows 专有二进制）、属于第三方产品而非本项目源码，不应进入版本库。下表说明"缺了什么、去哪补回"：

| 本地需要但仓库没有 | 是什么 | 为何不提交 | 如何补回 |
| --- | --- | --- | --- |
| `Mysql/`（原 ~1.1 GB） | MySQL 8.0.x 服务器安装目录 | 第三方二进制、Windows 专有、体积过大 | 见下方"方式一 / 方式二" |
| `Redis/`（原 ~47 MB） | Redis 服务器二进制 + 运行时数据 | 同上；`dump.rdb` 为运行时缓存数据，可丢弃 | 见下方"方式一 / 方式二" |
| `node_js/`（原 ~105 MB） | Node.js 运行时 | 第三方运行时，应由读者自备 | 安装 Node.js 24（见下方方式二） |
| `frontend/xwzx-news/node_modules/` | 前端依赖 | 可由 `npm install` 重建 | 前端目录执行 `npm install` |
| `backend/__pycache__/` | Python 编译缓存 | 运行后端时自动生成 | 无需处理 |
| `~$Readme.docx`、`~WRLxxxx.tmp` 等 | Office 临时锁文件 | 非项目内容 | 忽略 |

> 说明：`news_database/database.sql` **已**提交，包含全部建表语句（及少量示例数据）。克隆仓库后导入即可获得数据库结构，无需再从别处找。

### 方式一：Docker 一键补回 MySQL + Redis（推荐，跨平台）

仓库根目录已提供 `docker-compose.yml`，一条命令即可起好 MySQL 8.0 与 Redis 7：

```bash
docker compose up -d
```

启动后默认连接信息：

- MySQL：端口 `3306`，账号 `root`，密码 `123456`，默认库 `news_app`
- Redis：端口 `6379`

随后把表结构导入数据库：

```bash
docker compose exec -T mysql mysql -uroot -p123456 news_app < news_database/database.sql
```

> 没有 Docker 的 Windows 用户，改用下方"方式二"。

### 方式二：本地原生安装（以 Windows 为例）

1. **MySQL 8.0.x**：用官方安装包或压缩版安装，启动服务后把 `news_database/database.sql` 导入 `news_app` 库（命令见上方"环境准备"第 3 步）。
2. **Redis**：Windows 可用 Memurai 或微软归档版，启动 `redis-server`，默认端口 `6379`。
3. **Node.js 24**：从 nodejs.org 下载安装，或用 `nvm install 24`；进入 `frontend/xwzx-news` 执行 `npm install` 安装前端依赖。
4. **Python 依赖**：`pip install -r requirements.txt`（详见"环境准备"第 1–2 步）。

### 安全提示（配置已走环境变量）

数据库连接信息已从硬编码改为读取环境变量，并保留本地开发默认值，**仓库内不落真实密码**：

- MySQL：`DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` / `DB_NAME`（默认 `root` / `123456` / `localhost` / `3306` / `news_app`）
- Redis：`REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` / `REDIS_PASSWORD`（默认 `localhost` / `6379` / `0` / 无密码）

公开仓库前，复制 `.env.example` 为 `.env` 并覆盖上述变量即可；真实 `.env` 不要提交（已由仓库根目录的 `.gitignore` 排除）。若用 Docker，`docker-compose.yml` 中的 MySQL 密码与这里默认值保持一致。

## 附录：

### 认证方式

大部分接口需要认证，认证通过在请求头中添加 Authorization 字段实现：

`Authorization: token值`

### 响应格式

所有接口返回 JSON 格式数据，通用响应结构如下：

`{ "code": 200, "message": "success", "data": {} }`

### api 接口总览

1.用户管理模块 /api/user

|          |                    |              |                  |
|----------|--------------------|--------------|------------------|
| **方法** | **路径**           | **说明**     | **是否需要登录** |
| POST     | /api/user/register | 用户注册     | 否               |
| POST     | /api/user/login    | 用户登录     | 否               |
| GET      | /api/user/info     | 获取用户信息 | 是               |
| PUT      | /api/user/update   | 更新用户信息 | 是               |
| PUT      | /api/user/password | 修改用户密码 | 是               |

2.新闻模块 /api/news

| 方法 | 路径 | 说明 | 是否需要登录 |
| --- | --- | --- | --- |
| GET | /api/news/categories | 获取新闻分类列表 | 否 |
| GET | /api/news/list?categoryId=&page=&pageSize= | 获取新闻列表（分页） | 否 |
| GET | /api/news/detail?id= | 获取新闻详情（浏览量+1） | 否 |

3.收藏模块 /api/favorite

|  |  |  |  |
|----|----|----|----|
| **方法** | **路径** | **说明** | **是否需要登录** |
| GET | /api/favorite/check?newsId= | 检查新闻收藏状态 | 是 |
| POST | /api/favorite/add | 添加收藏 | 是 |
| DELETE | /api/favorite/remove?newsId= | 取消收藏 | 是 |
| GET | /api/favorite/list?page=&pageSize= | 获取收藏列表 | 是 |
| DELETE | /api/favorite/clear | 清空所有收藏 | 是 |

4.浏览历史模块 /api/history

|  |  |  |  |
|----|----|----|----|
| **方法** | **路径** | **说明** | **是否需要登录** |
| POST | /api/history/add | 添加浏览记录 | 是 |
| GET | /api/history/list?page=&pageSize= | 获取浏览历史列表 | 是 |
| DELETE | /api/history/delete/{history_id} | 删除单条浏览记录 | 是 |
| DELETE | /api/history/clear | 清空浏览历史 | 是 |

### 缓存策略

缓存只用在 news(新闻)模块,模式是 Cache-Aside(旁路缓存):先查 Redis,命中直接返回;未命中就查 MySQL,再把结果写回 Redis。缓存读写逻辑集中在 crud/news_cache.py(业务编排) + cache/news_cache.py(键名管理) + config/cache_conf.py(Redis 连接与基础读写)。

|  |  |  |  |
|----|----|----|----|
| **缓存内容** | **Redis Key** | **过期时间** | **说明** |
| 新闻分类列表 | news:categories | **7200 秒** | 分类变化极少,缓存最久 |
| 新闻列表 | news_list:{categoryId\|all}:{page}{size} | **1800 秒** | 按分类/分页组合缓存 |
| 新闻详情 | news:{newsId} | **1800 秒** | 单条新闻 |
| 相关新闻推荐 | news:{newsId}:{categoryId}:{limit} | **1800 秒** | 同类目按浏览量+时间排序取前 N 条 |
