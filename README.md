# 招聘求职网站 - 原型项目

一个基于 Vue 3 + Flask 的招聘求职网站原型，包含求职者端和企业端功能。

## 技术栈

### 后端
- Python 3.8+
- Flask 3.0
- Flask-SQLAlchemy (SQLite)
- Flask-JWT-Extended (认证)
- Flask-CORS (跨域)

### 前端
- Vue 3
- Vite
- Element Plus (UI组件库)
- Vue Router
- Pinia (状态管理)
- Axios

## 项目结构

```
zhaopin/
├── backend/                    # Flask 后端
│   ├── app.py                  # 应用入口
│   ├── config.py               # 配置
│   ├── models.py               # 数据库模型
│   ├── requirements.txt        # Python依赖
│   └── routes/                 # API路由
│       ├── auth.py             # 认证接口
│       ├── jobs.py             # 职位接口
│       ├── resumes.py          # 简历接口
│       └── applications.py     # 投递接口
│
├── frontend/                   # Vue 前端
│   ├── src/
│   │   ├── api/                # API封装
│   │   ├── components/         # 公共组件
│   │   ├── router/             # 路由配置
│   │   ├── stores/             # Pinia状态管理
│   │   └── views/              # 页面组件
│   │       ├── Home.vue        # 首页
│   │       ├── Login.vue       # 登录
│   │       ├── Register.vue    # 注册
│   │       ├── JobList.vue     # 职位列表
│   │       ├── JobDetail.vue   # 职位详情
│   │       ├── Resume.vue      # 我的简历
│   │       ├── MyApplications.vue  # 投递记录
│   │       └── company/        # 企业端页面
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 快速开始

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境（可选但推荐）
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务器
python app.py
```

后端服务将运行在 `http://localhost:5000`

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将运行在 `http://localhost:5173`

## 功能列表

### 求职者端
- ✅ 用户注册/登录（区分求职者和企业）
- ✅ 浏览职位列表、搜索职位
- ✅ 查看职位详情
- ✅ 投递简历
- ✅ 编辑个人简历
- ✅ 查看投递记录

### 企业端
- ✅ 发布职位
- ✅ 管理职位（编辑、上架/下架、删除）
- ✅ 查看收到的简历
- ✅ 接受/拒绝候选人

## API 接口

### 认证
- `POST /api/auth/register` - 注册
- `POST /api/auth/login` - 登录
- `GET /api/auth/me` - 获取当前用户

### 职位
- `GET /api/jobs` - 职位列表
- `GET /api/jobs/:id` - 职位详情
- `POST /api/jobs` - 发布职位
- `PUT /api/jobs/:id` - 更新职位
- `DELETE /api/jobs/:id` - 删除职位
- `GET /api/jobs/my` - 我的职位（企业）

### 简历
- `GET /api/resume` - 获取我的简历
- `POST /api/resume` - 保存简历

### 投递
- `POST /api/applications` - 投递简历
- `GET /api/applications/my` - 我的投递记录
- `GET /api/applications/received` - 收到的简历（企业）
- `PUT /api/applications/:id` - 更新投递状态

## 账号说明

### 注册求职者
- 选择"我要找工作"
- 填写用户名、邮箱、密码

### 注册企业用户
- 选择"我要招人"
- 填写用户名、邮箱、密码
- 填写公司名称（必填）
- 可选填行业、地址、简介

## 开发计划

- [x] Day 1: 项目初始化、数据库设计、用户认证
- [x] Day 2: 求职者端功能（职位搜索、简历管理）
- [x] Day 3: 企业端功能（职位管理、简历筛选）
- [x] Day 4: 投递系统、联调优化

## 注意事项

1. **数据存储**：使用 SQLite，数据保存在 `backend/instance/jobs.db`，可直接删除重建
2. **跨域配置**：前端已配置代理，开发时无需担心跨域问题
3. **JWT Token**：登录后token保存在 localStorage，有效期24小时

## 下一步可扩展

- [ ] 上传头像/公司Logo
- [ ] 富文本编辑器编辑职位描述
- [ ] 简历PDF导出
- [ ] 站内消息通知
- [ ] 数据统计仪表盘
- [ ] 高级搜索筛选（薪资范围、工作年限等）
