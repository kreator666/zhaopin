# 大学生社区网站改造计划

## 项目定位转变

**从**: 招聘求职网站  
**到**: 面向应届毕业生和在校大学生的综合社区平台

---

## 一、新架构概览

### 五大核心板块

```
┌─────────────────────────────────────────────────────────────┐
│                    大学生社区平台                            │
├─────────────┬─────────────┬─────────────┬─────────────┬─────┤
│  个人主页   │   求职就业   │   培训学习   │   交友社交   │ 跳蚤 │
│  (Profile)  │   (Jobs)    │  (Training) │ (Social)    │市场  │
├─────────────┼─────────────┼─────────────┼─────────────┼─────┤
│ • 个人资料  │ • 职位搜索   │ • 课程列表   │ • 校友圈    │ • 二 │
│ • 动态时间线 │ • 简历管理   │ • 学习小组   │ • 兴趣圈子  │   手 │
│ • 成就展示  │ • 投递记录   │ • 资料分享   │ • 活动发布  │   交 │
│ • 技能认证  │ • 面试经验   │ • 考证信息   │ • 约伴功能  │   易 │
│ • 收藏关注  │ • 企业宣讲   │ • 导师问答   │ • 私信聊天  │     │
└─────────────┴─────────────┴─────────────┴─────────────┴─────┘
```

---

## 二、数据库模型改造

### 2.1 用户体系扩展

```python
# 改造后的 User 模型
class User(db.Model):
    __tablename__ = 'users'
    
    # 原有字段保留
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 【改造】角色系统扩展
    role = db.Column(db.String(20), nullable=False, default='student')  
    # student: 在校学生/应届生
    # alumni: 校友
    # company: 企业HR
    # admin: 管理员
    
    # 【新增】学生认证信息
    student_verified = db.Column(db.Boolean, default=False)
    school_name = db.Column(db.String(100))      # 学校名称
    major = db.Column(db.String(100))            # 专业
    student_id = db.Column(db.String(50))        # 学号（用于认证）
    enrollment_year = db.Column(db.Integer)      # 入学年份
    graduation_year = db.Column(db.Integer)      # 毕业年份
    
    # 【新增】社区活跃度
    reputation = db.Column(db.Integer, default=0)     # 社区声望值
    post_count = db.Column(db.Integer, default=0)     # 发帖数
    follower_count = db.Column(db.Integer, default=0) # 粉丝数
    following_count = db.Column(db.Integer, default=0)# 关注数
    
    # 【新增】个人设置
    avatar_url = db.Column(db.String(500))
    cover_url = db.Column(db.String(500))
    bio = db.Column(db.Text)                     # 个人签名
    is_public = db.Column(db.Boolean, default=True)  # 资料公开性


# 【新增】用户关注关系表
class UserFollow(db.Model):
    __tablename__ = 'user_follows'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 唯一约束：不能重复关注
    __table_args__ = (db.UniqueConstraint('follower_id', 'following_id'),)


# 【新增】用户动态表（时间线）
class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  
    # types: post, like, comment, share, follow, job_apply, 
    #        training_enroll, flea_publish, friend_connect
    
    target_id = db.Column(db.Integer)            # 关联的目标ID
    target_type = db.Column(db.String(50))       # 目标类型
    content = db.Column(db.Text)                 # 动态内容（可选）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 2.2 个人主页模块

```python
# 【新增】用户技能认证
class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(50), nullable=False)  # 技能名称
    proficiency = db.Column(db.Integer)                     # 熟练度 1-5
    certification = db.Column(db.String(200))               # 相关证书
    verified = db.Column(db.Boolean, default=False)         # 是否认证
    

# 【新增】用户成就徽章
class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_type = db.Column(db.String(50), nullable=False)
    # types: active_poster, popular_user, job_hunter, 
    #        training_master, social_butterfly, flea_vendor
    badge_name = db.Column(db.String(100))
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】用户收藏表（统一收藏各类内容）
class UserFavorite(db.Model):
    __tablename__ = 'user_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(50), nullable=False)  
    # types: job, training, post, flea_item
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 2.3 求职模块（保留+扩展）

```python
# 保留现有 Job, Company, Application 模型
# 【扩展】面试经验分享
class InterviewExperience(db.Model):
    __tablename__ = 'interview_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100))
    experience_type = db.Column(db.String(20))  # interview, written_test
    content = db.Column(db.Text, nullable=False)  # 经验内容
    difficulty = db.Column(db.Integer)           # 难度 1-5
    result = db.Column(db.String(20))            # offer, rejected, pending
    helpful_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='approved')  # pending, approved, rejected


# 【扩展】校园宣讲会
class CampusTalk(db.Model):
    __tablename__ = 'campus_talks'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))         # 宣讲地点
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    description = db.Column(db.Text)
    registration_url = db.Column(db.String(500))
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 2.4 培训学习模块（全新）

```python
# 【新增】培训课程
class TrainingCourse(db.Model):
    __tablename__ = 'training_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    # categories: programming, language, exam_prep, career, hobby
    
    provider = db.Column(db.String(100))         # 提供方
    instructor = db.Column(db.String(100))       # 讲师
    price = db.Column(db.Float, default=0)       # 价格，0表示免费
    original_price = db.Column(db.Float)
    
    duration = db.Column(db.String(50))          # 课程时长
    level = db.Column(db.String(20))             # beginner, intermediate, advanced
    
    cover_image = db.Column(db.String(500))
    detail_url = db.Column(db.String(500))       # 课程详情链接
    
    enrolled_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=5.0)    # 评分
    review_count = db.Column(db.Integer, default=0)
    
    is_online = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(200))         # 线下课程地址
    
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    status = db.Column(db.String(20), default='active')  # active, ended, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】课程报名记录
class CourseEnrollment(db.Model):
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('training_courses.id'), nullable=False)
    status = db.Column(db.String(20), default='enrolled')  # enrolled, completed, dropped
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    review_content = db.Column(db.Text)
    review_rating = db.Column(db.Integer)


# 【新增】学习资料分享
class StudyMaterial(db.Model):
    __tablename__ = 'study_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))          # 资料分类
    file_url = db.Column(db.String(500))         # 文件链接
    file_type = db.Column(db.String(20))         # pdf, video, doc, etc.
    file_size = db.Column(db.String(20))         # 文件大小
    download_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】考证信息
class CertificationInfo(db.Model):
    __tablename__ = 'certification_infos'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)      # 证书名称
    category = db.Column(db.String(50))                   # 类别
    description = db.Column(db.Text)
    organizer = db.Column(db.String(100))                 # 主办单位
    registration_start = db.Column(db.Date)
    registration_end = db.Column(db.Date)
    exam_date = db.Column(db.Date)
    registration_url = db.Column(db.String(500))
    fee = db.Column(db.Float)
    requirements = db.Column(db.Text)                     # 报考条件
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### 2.5 交友社交模块（全新）

```python
# 【新增】帖子/动态（校友圈）
class SocialPost(db.Model):
    __tablename__ = 'social_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    post_type = db.Column(db.String(20), default='text')
    # types: text, image, video, poll, article
    
    images = db.Column(db.Text)                  # 图片URL列表，JSON格式
    
    # 圈子关联
    circle_id = db.Column(db.Integer, db.ForeignKey('social_circles.id'))
    
    # 互动数据
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    
    is_anonymous = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, hidden, deleted
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 【新增】帖子评论
class PostComment(db.Model):
    __tablename__ = 'post_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('social_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('post_comments.id'))  # 回复评论
    content = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】点赞记录
class PostLike(db.Model):
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(20), nullable=False)  # post, comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'target_id', 'target_type'),)


# 【新增】兴趣圈子
class SocialCircle(db.Model):
    __tablename__ = 'social_circles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))          # 圈子分类
    # categories: study, career, hobby, campus, city
    
    icon_url = db.Column(db.String(500))
    cover_url = db.Column(db.String(500))
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    member_count = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)
    
    is_public = db.Column(db.Boolean, default=True)  # 是否公开圈子
    need_approval = db.Column(db.Boolean, default=False)  # 加入是否需要审批
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】圈子成员
class CircleMember(db.Model):
    __tablename__ = 'circle_members'
    
    id = db.Column(db.Integer, primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('social_circles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # member, admin, owner
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('circle_id', 'user_id'),)


# 【新增】活动/约伴
class SocialEvent(db.Model):
    __tablename__ = 'social_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))        # study, sport, travel, meal, etc.
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    location = db.Column(db.String(200))
    location_lat = db.Column(db.Float)           # 纬度
    location_lng = db.Column(db.Float)           # 经度
    
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(20), default='open')  # open, full, ended, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】活动参与者
class EventParticipant(db.Model):
    __tablename__ = 'event_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('social_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='joined')  # joined, cancelled
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】私信/聊天
class PrivateMessage(db.Model):
    __tablename__ = 'private_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, image
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# 【新增】聊天会话（用于汇总未读消息）
class ChatConversation(db.Model):
    __tablename__ = 'chat_conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_message_id = db.Column(db.Integer, db.ForeignKey('private_messages.id'))
    last_message_at = db.Column(db.DateTime)
    unread_count_user1 = db.Column(db.Integer, default=0)
    unread_count_user2 = db.Column(db.Integer, default=0)
    
    __table_args__ = (db.UniqueConstraint('user1_id', 'user2_id'),)
```

### 2.6 跳蚤市场模块（全新）

```python
# 【新增】二手物品
class FleaItem(db.Model):
    __tablename__ = 'flea_items'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    # categories: book, electronics, bike, dorm, ticket, other
    
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    
    condition = db.Column(db.String(20))         # new, like_new, good, fair
    
    images = db.Column(db.Text)                  # 图片URL列表，JSON格式
    
    # 交易信息
    trade_location = db.Column(db.String(200))   # 交易地点
    trade_method = db.Column(db.String(50))      # face_to_face, campus_delivery, express
    
    view_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(20), default='on_sale')  # on_sale, reserved, sold, removed
    
    is_bargain_allowed = db.Column(db.Boolean, default=True)  # 是否接受砍价
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sold_at = db.Column(db.DateTime)


# 【新增】物品收藏
class FleaFavorite(db.Model):
    __tablename__ = 'flea_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('flea_items.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'item_id'),)


# 【新增】求购信息
class FleaWanted(db.Model):
    __tablename__ = 'flea_wanted'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    max_price = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, fulfilled, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 三、API 接口规划

### 3.1 路由结构

```
backend/routes/
├── __init__.py
├── auth.py              # 认证（保留+扩展）
├── users.py             # 【新增】用户管理
├── profile.py           # 【新增】个人主页
├── jobs.py              # 求职（保留+扩展）
├── companies.py         # 【新增】企业相关
├── interview.py         # 【新增】面试经验
├── training.py          # 【新增】培训课程
├── study_material.py    # 【新增】学习资料
├── certification.py     # 【新增】考证信息
├── social.py            # 【新增】社交动态
├── circles.py           # 【新增】兴趣圈子
├── events.py            # 【新增】活动约伴
├── messages.py          # 【新增】私信聊天
├── flea.py              # 【新增】跳蚤市场
├── search.py            # 【新增】全局搜索
└── upload.py            # 【新增】文件上传
```

### 3.2 API 详细设计

详见后续章节...

---

## 四、前端页面架构

### 4.1 路由结构

```
frontend/src/views/
├── Home.vue                    # 首页（综合信息流）
├── Login.vue / Register.vue    # 登录/注册
│
├── profile/                    # 个人主页模块
│   ├── Profile.vue             # 个人主页
│   ├── ProfileEdit.vue         # 编辑资料
│   ├── MyPosts.vue             # 我的动态
│   ├── MyFavorites.vue         # 我的收藏
│   ├── MyFollowers.vue         # 粉丝/关注
│   └── Settings.vue            # 账号设置
│
├── jobs/                       # 求职模块
│   ├── JobList.vue             # 职位列表
│   ├── JobDetail.vue           # 职位详情
│   ├── MyApplications.vue      # 我的投递
│   ├── InterviewList.vue       # 【新增】面经列表
│   ├── InterviewDetail.vue     # 【新增】面经详情
│   └── CampusTalk.vue          # 【新增】宣讲会
│
├── training/                   # 【新增】培训模块
│   ├── CourseList.vue          # 课程列表
│   ├── CourseDetail.vue        # 课程详情
│   ├── MaterialList.vue        # 资料分享
│   ├── MaterialUpload.vue      # 上传资料
│   └── Certification.vue       # 考证信息
│
├── social/                     # 【新增】社交模块
│   ├── Feed.vue                # 动态流（校友圈）
│   ├── PostDetail.vue          # 帖子详情
│   ├── CircleList.vue          # 圈子列表
│   ├── CircleDetail.vue        # 圈子详情
│   ├── EventList.vue           # 活动列表
│   ├── EventDetail.vue         # 活动详情
│   └── Chat.vue                # 私信聊天
│
├── flea/                       # 【新增】跳蚤市场
│   ├── ItemList.vue            # 物品列表
│   ├── ItemDetail.vue          # 物品详情
│   ├── ItemPublish.vue         # 发布物品
│   ├── ItemManage.vue          # 我的发布
│   └── WantedList.vue          # 求购列表
│
└── company/                    # 企业端（保留）
    └── ...
```

### 4.2 布局组件

```
frontend/src/components/layout/
├── MainLayout.vue              # 主布局（含导航）
├── SimpleLayout.vue            # 简洁布局（登录页）
├── AppHeader.vue               # 顶部导航栏
├── AppFooter.vue               # 页脚
├── SideMenu.vue                # 侧边菜单
├── MobileNav.vue               # 移动端底部导航
└── NotificationCenter.vue      # 消息通知中心
```

---

## 五、开发优先级和里程碑

### 阶段一：基础架构改造（2周）
**目标**: 完成数据库迁移和基础架构

| 任务 | 工作量 | 依赖 |
|------|--------|------|
| 设计新数据库模型 | 2天 | - |
| 编写数据库迁移脚本 | 1天 | 模型设计 |
| 扩展用户认证系统 | 2天 | - |
| 搭建新的前端路由结构 | 2天 | - |
| 设计通用组件库 | 3天 | - |
| 文件上传服务 | 2天 | - |

**交付物**:
- 新的 `models.py` 
- 数据库迁移脚本
- 前端基础布局组件

### 阶段二：个人主页 + 求职（2周）
**目标**: 完成用户体系和求职模块改造

| 任务 | 工作量 | 依赖 |
|------|--------|------|
| 用户资料管理API | 3天 | 阶段一 |
| 用户关注/粉丝功能 | 2天 | 用户API |
| 个人主页页面 | 3天 | 用户API |
| 动态时间线功能 | 2天 | 用户API |
| 求职模块优化 | 3天 | - |
| 面经/宣讲会功能 | 3天 | 求职模块 |

**交付物**:
- 完整的用户系统
- 改造后的求职模块

### 阶段三：培训学习模块（1.5周）
**目标**: 完成培训板块

| 任务 | 工作量 | 依赖 |
|------|--------|------|
| 课程管理API | 2天 | 阶段一 |
| 学习资料API | 2天 | 上传服务 |
| 考证信息API | 1天 | - |
| 课程列表/详情页 | 2天 | API |
| 学习小组功能 | 2天 | 社交API |

**交付物**:
- 培训课程系统
- 资料分享功能

### 阶段四：社交交友模块（2周）
**目标**: 完成社交核心功能

| 任务 | 工作量 | 依赖 |
|------|--------|------|
| 帖子/动态API | 3天 | 阶段一 |
| 圈子管理API | 2天 | 动态API |
| 活动约伴API | 2天 | - |
| 私信聊天API | 3天 | WebSocket |
| 动态流页面 | 3天 | API |
| 圈子功能页面 | 2天 | API |
| 聊天界面 | 3天 | API |

**交付物**:
- 完整的社交系统
- 实时聊天功能

### 阶段五：跳蚤市场（1周）
**目标**: 完成二手交易板块

| 任务 | 工作量 | 依赖 |
|------|--------|------|
| 物品管理API | 2天 | 上传服务 |
| 求购信息API | 1天 | - |
| 物品列表/详情页 | 2天 | API |
| 发布/管理页面 | 2天 | API |

**交付物**:
- 完整的跳蚤市场功能

### 阶段六：优化和上线（1周）
**目标**: 性能优化和Bug修复

| 任务 | 工作量 |
|------|--------|
| 性能优化 | 2天 |
| 移动端适配 | 2天 |
| 安全加固 | 2天 |
| Bug修复 | 持续 |

---

## 六、技术选型补充

### 新增依赖

**后端**:
```txt
# WebSocket (实时聊天)
flask-socketio==5.3.0
python-socketio==5.9.0

# 搜索
flask-whooshalchemy==0.8.4

# 图片处理
Pillow==10.1.0

# 缓存
flask-caching==2.1.0
redis==5.0.1
```

**前端**:
```json
{
  "dependencies": {
    "vue": "^3.4.15",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.5",
    "element-plus": "^2.5.1",
    "@element-plus/icons-vue": "^2.3.1",
    
    "// 新增": "",
    "socket.io-client": "^4.7.4",      // WebSocket客户端
    "vue-infinite-scroll": "^2.0.2",   // 无限滚动
    "vue-lazyload": "^3.0.0",          // 图片懒加载
    "@vueuse/core": "^10.7.2",         // 工具函数
    "dayjs": "^1.11.10",               // 日期处理
    "marked": "^11.1.1",               // Markdown
    "cropperjs": "^1.6.1"              // 图片裁剪
  }
}
```

---

## 七、数据迁移策略

### 现有数据保留

1. **用户数据**: 保留，添加新字段默认值
2. **公司数据**: 保留
3. **职位数据**: 保留
4. **简历/投递**: 保留

### 迁移脚本示例

```python
# migrations/migrate_to_community.py
"""
从招聘网站迁移到社区网站的数据迁移脚本
"""

def migrate_users():
    """迁移用户数据"""
    # 1. 添加新字段
    # 2. 根据现有数据推断 graduation_year
    # 3. 设置默认 reputation = 0
    pass

def migrate_jobs():
    """职位数据保持不变"""
    pass

def main():
    print("开始数据迁移...")
    migrate_users()
    migrate_jobs()
    print("迁移完成！")

if __name__ == '__main__':
    main()
```

---

## 八、风险评估

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|----------|
| 开发周期延长 | 中 | 高 | 分阶段交付，MVP优先 |
| 数据迁移丢失 | 低 | 高 | 完整备份，灰度迁移 |
| 性能问题 | 中 | 中 | 缓存策略，分页加载 |
| 用户不适应 | 中 | 中 | 保留原功能，逐步引导 |

---

**文档版本**: v1.0  
**制定时间**: 2024年  
**预计总工期**: 9-10周
