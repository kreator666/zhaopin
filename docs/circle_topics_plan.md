# 兴趣圈子话题功能开发计划

## 一、功能需求

| 功能模块 | 需求描述 | 优先级 |
|---------|---------|--------|
| 话题管理 | 在圈子内创建话题 | P0 |
| 标签系统 | 话题分类标签，支持搜索筛选 | P0 |
| 可见范围 | 全部学校可见 / 仅本校可见 | P0 |
| 讨论跟帖 | 话题下可回复讨论 | P0 |
| 话题终结 | 发起者可标记话题为"已解决"/"已关闭" | P1 |
| 话题搜索 | 按标签、关键词、时间筛选 | P1 |

## 二、数据库表结构

### 1. circle_topics 话题表
```sql
- id: 主键
- circle_id: 所属圈子ID
- user_id: 发布者ID
- title: 话题标题
- content: 话题内容
- tags: 标签JSON数组
- visibility: public(全站)/school_only(仅本校)
- status: open(开放)/closed(已关闭)/solved(已解决)
- is_pinned: 是否置顶
- view_count: 浏览数
- reply_count: 回复数
- last_reply_at: 最后回复时间
- created_at/updated_at
```

### 2. circle_topic_replies 回复表
```sql
- id: 主键
- topic_id: 话题ID
- user_id: 回复者ID
- parent_id: 父回复ID（楼中楼）
- content: 回复内容
- is_accepted: 是否被采纳为最佳答案
- created_at
```

## 三、API设计

### 话题管理
- GET /api/circles/:id/topics - 获取话题列表
- POST /api/circles/:id/topics - 创建话题
- GET /api/circles/topics/:topic_id - 获取详情
- PUT /api/circles/topics/:topic_id - 编辑话题
- DELETE /api/circles/topics/:topic_id - 删除话题
- POST /api/circles/topics/:topic_id/close - 关闭话题
- POST /api/circles/topics/:topic_id/solve - 标记已解决

### 话题回复
- GET /api/circles/topics/:topic_id/replies - 获取回复
- POST /api/circles/topics/:topic_id/replies - 发表回复
- DELETE /api/circles/replies/:reply_id - 删除回复
- POST /api/circles/replies/:reply_id/accept - 采纳最佳答案

## 四、开发阶段

### Phase 1：基础功能（P0）
1. 数据库表创建
2. 后端API - 话题CRUD
3. 后端API - 回复功能
4. 前端 - 话题列表展示
5. 前端 - 发布话题弹窗
6. 前端 - 话题详情页

### Phase 2：标签与搜索（P1）
1. 标签系统后端
2. 话题搜索API
3. 前端标签组件

### Phase 3：进阶功能（P1）
1. 话题状态管理
2. 最佳答案采纳
3. 话题置顶
