# 📰 Headline_News — 新闻资讯系统

基于 **FastAPI + Vue3(React)** 前后端分离架构的新闻资讯应用后端服务，提供新闻浏览、用户认证、收藏管理和浏览历史等功能。

---

## 📑 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [环境准备](#环境准备)
- [运行项目](#运行项目)
- [API 文档](#api-文档)
  - [认证方式](#认证方式)
  - [响应格式](#响应格式)
  - [接口总览](#接口总览)
- [缓存策略](#缓存策略)
- [仓库未包含的内容与补回方法](#仓库未包含的内容与补回方法)

---

## 技术栈

| 类别 | 技术 |
| --- | --- |
| 语言 | Python 3.12 |
| Web 框架 | FastAPI — 异步 Web 框架 |
| ORM | SQLAlchemy 2.0 — 异步 ORM |
| 数据库 | MySQL — 关系型数据库（通过 aiomysql 异步驱动连接） |
| 缓存 | Redis — 缓存中间件（通过 redis.asyncio 异步客户端连接） |
| 密码加密 | Passlib + bcrypt |
| 数据校验 | Pydantic v2 — 请求数据校验与响应序列化 |
| ASGI 服务器 | Uvicorn |

---

## 项目结构

```
Headline_News/
│
├── backend/                          # 后端根目录（FastAPI）
│   ├── main.py                       # 应用入口，创建 FastAPI 实例、注册路由与异常处理器
│   ├── requirements.txt              # Python 依赖清单
│   ├── test_main.http                # REST Client 接口测试脚本（IDE 内调试用）
│   │
│   ├── config/                       # 配置层
│   │   ├── db_conf.py                # MySQL 异步引擎配置 + 数据库会话依赖注入
│   │   └── cache_conf.py             # Redis 异步客户端 + 通用缓存读写函数
│   │
│   ├── models/                       # ORM 模型层（对应数据库表结构）
│   │   ├── news.py                   # News（新闻表）、Category（分类表）
│   │   ├── users.py                  # User（用户表）、UserToken（令牌表）
│   │   ├── favorite.py               # Favorite（收藏表）
│   │   └── history.py                # History（浏览历史表）
│   │
│   ├── schemas/                      # Pydantic 校验层（请求/响应模型）
│   │   ├── base.py                   # 公共基础模型（统一别名映射等配置）
│   │   ├── users.py                  # 用户相关模型（注册 / 登录 / 信息更新）
│   │   ├── favorite.py               # 收藏相关模型
│   │   └── history.py                # 浏览历史相关模型
│   │
│   ├── crud/                         # 数据访问层
│   │   ├── news.py                   # 新闻基础数据库操作（列表 / 详情 / 计数）
│   │   ├── news_cache.py             # 带缓存优先逻辑的新闻操作（路由实际调用此文件）
│   │   ├── users.py                  # 用户 CRUD + 令牌生成 / 校验
│   │   ├── favorite.py               # 收藏增删查 / 清空
│   │   └── history.py                # 浏览历史记录 / 查询 / 删除 / 清空
│   │
│   ├── routers/                      # 路由层（对外 API 端点）
│   │   ├── news.py                   # 新闻接口：/api/news/*
│   │   ├── users.py                  # 用户接口：/api/user/*
│   │   ├── favorite.py               # 收藏接口：/api/favorite/*
│   │   └── history.py                # 历史记录接口：/api/history/*
│   │
│   ├── cache/                        # 缓存键管理层
│   │   └── news_cache.py             # 缓存键名生成与读写封装（分类 / 列表 / 详情 / 推荐）
│   │
│   └── utils/                        # 公共工具层
│       ├── auth.py                   # JWT 鉴权依赖（从 Authorization 头提取 token）
│       ├── security.py               # bcrypt 密码哈希与校验
│       ├── response.py               # 统一响应格式 { code, message, data }
│       ├── exception.py              # 分级异常处理器实现
│       └── exception_handles.py      # 异常处理器注册到 app（被 main.py 调用）
│
├── frontend/xwzx-news/               # 前端根目录（Vue3）
│   ├── index.html                    # 入口 HTML
│   ├── package.json                  # 前端依赖清单
│   └── src/
│       ├── main.js                   # Vue 应用入口
│       ├── App.vue                   # 根组件
│       ├── router/index.js           # 路由配置
│       ├── store/                    # Pinia 状态管理
│       │   ├── index.js
│       │   ├── modules/news.js       # 新闻状态
│       │   ├── modules/user.js       # 用户状态
│       │   ├── modules/favorite.js   # 收藏状态
│       │   ├── modules/history.js    # 历史状态
│       │   ├── theme.js              # 主题切换
│       │   └── language.js           # 语言切换
│       ├── views/                    # 页面视图
│       │   ├── Home.vue              # 首页
│       │   ├── Category.vue          # 分类页
│       │   ├── NewsDetail.vue        # 新闻详情
│       │   ├── Favorite.vue          # 我的收藏
│       │   ├── History.vue           # 浏览历史
│       │   ├── Login.vue             # 登录
│       │   ├── Register.vue          # 注册
│       │   ├── My.vue                # 个人中心
│       │   ├── Profile.vue           # 个人资料
│       │   ├── Settings.vue          # 设置
│       │   └── AIChat.vue            # AI 对话
│       ├── components/               # 公共组件
│       │   ├── NewsItem.vue          # 新闻条目
│       │   ├── TabBar.vue            # 底部导航栏
│       │   └── HelloWorld.vue
│       ├── config/api.js             # API 请求封装
│       ├── i18n/                     # 国际化
│       │   ├── locales/zh-CN.js      # 中文语言包
│       │   └── locales/en-US.js      # 英文语言包
│       ├── assets/                   # 静态资源
│       └── style.css                 # 全局样式
│
├── news_database/
│   └── database.sql                  # 数据库建表语句 + 示例数据
│
├── docker-compose.yml                # Docker 编排（MySQL 8.0 + Redis 7）
├── .env.example                      # 环境变量模板（复制为 .env 使用）
├── .gitignore                        # Git 忽略规则
└── README.md                         # 项目说明文档（本文件）
```

---

## 环境准备

### 1. Python 环境

安装 Python 3.12+（推荐使用 Conda 或官方安装包），创建虚拟环境：

```bash
conda create -n fastapi_env python=3.12 -y
conda activate fastapi_env
```

### 2. 安装 Python 依赖

```bash
pip install -r backend/requirements.txt
```

> 国内用户可使用镜像源加速：
> ```bash
> pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 3. 启动 MySQL

#### 方式一：Docker 一键启动（推荐）

```bash
docker compose up -d
```

默认连接信息：端口 `3306`，账号 `root`，密码 `123456`，库 `news_app`

导入表结构：

```bash
docker compose exec -T mysql mysql -uroot -p123456 news_app < news_database/database.sql
```

#### 方式二：本地安装 MySQL 8.0.x

1. 本地安装 MySQL 8.0.x，确保已加入环境变量
2. 以管理员身份打开 cmd，启动 MySQL 服务：

```bash
net start mysql_news
```

3. 进入 MySQL 交互端创建数据库并导入：

```bash
mysql -u root -p
CREATE DATABASE IF NOT EXISTS news_app DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit
mysql -u root -p news_app < news_database/database.sql
```

> 注意：本项目的数据库名为 `news_app`，MySQL 服务名为 `mysql_news`（本地安装时按实际情况调整）。

### 4. 启动 Redis

#### 方式一：Docker（随上方 docker compose 已一并启动，无需额外操作）

#### 方式二：本地安装 Redis 7.x.x

```bash
redis-server.exe redis.windows.conf    # 在 Redis 目录下执行，默认端口 6379
```

### 5. 环境变量配置

MySQL 和 Redis 的连接信息通过环境变量配置，**已保留本地开发默认值，一般无需修改即可直接运行**：

- 复制 `.env.example` 为 `.env`（可选），按需覆盖以下变量：

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `DB_USER` | MySQL 用户名 | `root` |
| `DB_PASSWORD` | MySQL 密码 | `123456` |
| `DB_HOST` | MySQL 地址 | `localhost` |
| `DB_PORT` | MySQL 端口 | `3306` |
| `DB_NAME` | 数据库名 | `news_app` |
| `REDIS_HOST` | Redis 地址 | `localhost` |
| `REDIS_PORT` | Redis 端口 | `6379` |
| `REDIS_DB` | Redis 库编号 | `0` |
| `REDIS_PASSWORD` | Redis 密码 | 无（留空） |

> 配置代码位于 `config/db_conf.py` 与 `config/cache_conf.py`，可随时查看或修改默认值。

### 6. 安装前端依赖

```bash
cd frontend/xwzx-news
npm install
```

> 需要 Node.js 18+ 环境，从 [nodejs.org](https://nodejs.org) 下载或使用 nvm 管理。

---

## 运行项目

### 快速启动（完整流程）

按顺序依次执行以下命令：

```bash
# 1️⃣ 启动 MySQL（管理员 cmd）
net start mysql_news

# 2️⃣ 启动 Redis（Redis 目录下）
redis-server.exe redis.windows.conf

# 3️⃣ 启动前端（前端目录下）
cd frontend/xwzx-news
npm run dev

# 4️⃣ 启动后端（后端目录下，确保在 conda 虚拟环境中）
cd ../../backend
python main.py
```

启动成功标志：

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### 访问地址

| 服务 | 地址 | 说明 |
| --- | --- | --- |
| 后端 API | http://127.0.0.1:8000/docs | Swagger UI 接口文档 |
| 前端页面 | http://localhost:5173/ | Vue3 前端界面 |

---

## API 文档

### 认证方式

大部分接口需要登录认证，在请求头中添加 `Authorization` 字段：

```
Authorization: Bearer <token值>
```

> 登录接口 `/api/user/login` 成功后返回的 token 即可用于后续请求。

### 响应格式

所有接口返回统一的 JSON 格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 接口总览

#### 1. 用户管理模块 `/api/user`

| 方法 | 路径 | 说明 | 需要登录 |
| --- | --- | --- | --- |
| POST | /api/user/register | 用户注册 | ❌ |
| POST | /api/user/login | 用户登录 | ❌ |
| GET | /api/user/info | 获取用户信息 | ✅ |
| PUT | /api/user/update | 更新用户信息 | ✅ |
| PUT | /api/user/password | 修改用户密码 | ✅ |

#### 2. 新闻模块 `/api/news`

| 方法 | 路径 | 说明 | 需要登录 |
| --- | --- | --- | --- |
| GET | /api/news/categories | 获取新闻分类列表 | ❌ |
| GET | /api/news/list | 获取新闻列表（分页） | ❌ |
| GET | /api/news/detail | 获取新闻详情（浏览量+1） | ❌ |

#### 3. 收藏模块 `/api/favorite`

| 方法 | 路径 | 说明 | 需要登录 |
| --- | --- | --- | --- |
| GET | /api/favorite/check | 检查新闻收藏状态 | ✅ |
| POST | /api/favorite/add | 添加收藏 | ✅ |
| DELETE | /api/favorite/remove | 取消收藏 | ✅ |
| GET | /api/favorite/list | 获取收藏列表（分页） | ✅ |
| DELETE | /api/favorite/clear | 清空所有收藏 | ✅ |

#### 4. 浏览历史模块 `/api/history`

| 方法 | 路径 | 说明 | 需要登录 |
| --- | --- | --- | --- |
| POST | /api/history/add | 添加浏览记录 | ✅ |
| GET | /api/history/list | 获取浏览历史列表（分页） | ✅ |
| DELETE | /api/history/delete/{id} | 删除单条浏览记录 | ✅ |
| DELETE | /api/history/clear | 清空浏览历史 | ✅ |

---

## 缓存策略

缓存仅用于**新闻模块**，采用 **Cache-Aside（旁路缓存）** 模式：先查 Redis → 命中直接返回 → 未命中查 MySQL → 结果写回 Redis。

缓存逻辑分层如下：

| 层级 | 文件 | 职责 |
| --- | --- | --- |
| 键名管理 | `cache/news_cache.py` | 封装各场景的 Redis Key 生成规则 |
| 缓存读写 | `config/cache_conf.py` | Redis 连接与基础 get/set 操作 |
| 业务编排 | `crud/news_cache.py` | 按业务逻辑调用缓存/数据库，路由实际调用此层 |

| 缓存内容 | Redis Key 模板 | 过期时间 | 说明 |
| --- | --- | --- | --- |
| 新闻分类列表 | `news:categories` | **7200 秒（2 小时）** | 分类变化极少，缓存最久 |
| 新闻列表 | `news_list:{categoryId}:{page}:{size}` | **1800 秒（30 分钟）** | 按分类 + 分页组合缓存 |
| 新闻详情 | `news:{newsId}` | **1800 秒（30 分钟）** | 单条新闻（含浏览量+1） |
| 相关新闻推荐 | `news:{newsId}:{categoryId}:{limit}` | **1800 秒（30 分钟）** | 同类目按浏览量排序取前 N 条 |

---

## 仓库未包含的内容与补回方法

本仓库**只提交源码**，整体体积仅几百 KB。本地运行所需的二进制与依赖**没有放进 git**：

| 未包含内容 | 是什么 | 为何不提交 | 如何补回 |
| --- | --- | --- | --- |
| `Mysql/`（~1.1 GB） | MySQL 8.0 服务器安装目录 | 第三方二进制、Windows 专有、体积过大 | 见上方「方式一 / 方式二」 |
| `Redis/`（~47 MB） | Redis 服务器 + 运行时数据 dump.rdb | 同上；dump.rdb 可丢弃重建 | 见上方「方式一 / 方式二」 |
| `node_js/`（~105 MB） | Node.js 运行时 | 第三方运行时，读者自备 | 安装 Node.js 18+ |
| `frontend/.../node_modules/` | 前端 npm 依赖 | 可由 `npm install` 重建 | `cd frontend/xwzx-news && npm install` |
| `backend/__pycache__/` | Python 编译缓存 | 运行时自动生成 | 无需处理 |


> `news_database/database.sql` **已包含在仓库内**，克隆后直接导入即可获得完整的数据库表结构与示例数据。
