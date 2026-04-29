from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ==========================================
# 用户相关模型
# ==========================================

class User(db.Model):
    __tablename__ = 'users'
    
    # 基础字段（保留）
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 【改造】角色系统扩展
    # student: 在校学生/应届生
    # alumni: 校友  
    # company: 企业HR
    # admin: 管理员
    role = db.Column(db.String(20), nullable=False, default='student')
    
    # 【新增】学生认证信息
    student_verified = db.Column(db.Boolean, default=False)
    school_name = db.Column(db.String(100))      # 学校名称
    major = db.Column(db.String(100))            # 专业
    student_id = db.Column(db.String(50))        # 学号（用于认证）
    enrollment_year = db.Column(db.Integer)      # 入学年份
    graduation_year = db.Column(db.Integer)      # 毕业年份
    gender = db.Column(db.String(10))            # 性别
    
    # 【新增】社区活跃度
    reputation = db.Column(db.Integer, default=0)     # 社区声望值
    post_count = db.Column(db.Integer, default=0)     # 发帖数
    follower_count = db.Column(db.Integer, default=0) # 粉丝数
    following_count = db.Column(db.Integer, default=0)# 关注数
    
    # 【新增】个人展示
    avatar_url = db.Column(db.String(500))
    cover_url = db.Column(db.String(500))
    bio = db.Column(db.Text)                     # 个人签名/简介
    is_public = db.Column(db.Boolean, default=True)  # 资料公开性
    last_active_at = db.Column(db.DateTime)      # 最后活跃时间
    
    # 关联
    company = db.relationship('Company', backref='user', uselist=False, lazy=True)
    job_seeker_profile = db.relationship('JobSeekerProfile', backref='user', uselist=False, lazy=True)
    # skills 和 badges 通过 UserSkill/UserBadge 中的 backref 自动关联
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_profile=False, include_skills=False, include_badges=False, include_stats=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'school_name': self.school_name,
            'major': self.major,
            'enrollment_year': self.enrollment_year,
            'gender': self.gender,
            'graduation_year': self.graduation_year,
            'student_verified': self.student_verified,
            'avatar_url': self.avatar_url,
            'cover_url': self.cover_url,
            'bio': self.bio,
            'reputation': self.reputation,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'post_count': self.post_count,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active_at': self.last_active_at.isoformat() if self.last_active_at else None
        }
        if include_profile and self.job_seeker_profile:
            data['profile'] = self.job_seeker_profile.to_dict()
        if include_skills:
            data['skills'] = [skill.to_dict() for skill in self.skills]
        if include_badges:
            data['badges'] = [badge.to_dict() for badge in self.badges]
        return data


class UserFollow(db.Model):
    """用户关注关系表"""
    __tablename__ = 'user_follows'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 唯一约束：不能重复关注
    __table_args__ = (db.UniqueConstraint('follower_id', 'following_id', name='unique_follow'),)
    
    # 关联
    follower = db.relationship('User', foreign_keys=[follower_id], backref='following', lazy=True)
    following = db.relationship('User', foreign_keys=[following_id], backref='followers', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'following_id': self.following_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserActivity(db.Model):
    """用户动态（时间线）"""
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
    
    # 关联
    user = db.relationship('User', backref='activities', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'target_id': self.target_id,
            'target_type': self.target_type,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


class UserSkill(db.Model):
    """用户技能认证"""
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(50), nullable=False)
    proficiency = db.Column(db.Integer)          # 熟练度 1-5
    certification = db.Column(db.String(200))    # 相关证书
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='skills', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_name': self.skill_name,
            'proficiency': self.proficiency,
            'certification': self.certification,
            'verified': self.verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class UserBadge(db.Model):
    """用户成就徽章"""
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_type = db.Column(db.String(50), nullable=False)
    # types: active_poster, popular_user, job_hunter, 
    #        training_master, social_butterfly, flea_vendor
    badge_name = db.Column(db.String(100))
    badge_icon = db.Column(db.String(200))
    description = db.Column(db.Text)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='badges', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'badge_type': self.badge_type,
            'badge_name': self.badge_name,
            'badge_icon': self.badge_icon,
            'description': self.description,
            'awarded_at': self.awarded_at.isoformat() if self.awarded_at else None
        }


class UserFavorite(db.Model):
    """用户收藏（统一收藏各类内容）"""
    __tablename__ = 'user_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(50), nullable=False)
    # types: job, training, post, flea_item, material
    title = db.Column(db.String(200))            # 收藏时的标题（快照）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'target_id', 'target_type', name='unique_favorite'),)
    
    user = db.relationship('User', backref='favorites', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'target_id': self.target_id,
            'target_type': self.target_type,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ==========================================
# 求职相关模型（保留+扩展）
# ==========================================

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    scale = db.Column(db.String(50))             # 公司规模
    website = db.Column(db.String(200))
    logo = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    jobs = db.relationship('Job', backref='company', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'industry': self.industry,
            'scale': self.scale,
            'website': self.website,
            'logo': self.logo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class JobSeekerProfile(db.Model):
    """求职者档案（保留，作为简历扩展）"""
    __tablename__ = 'job_seeker_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    location = db.Column(db.String(100))
    summary = db.Column(db.Text)                 # 个人简介
    experience_text = db.Column(db.Text)         # 工作经历（简化版）
    education_text = db.Column(db.Text)          # 教育经历（简化版）
    skills = db.Column(db.String(500))           # 技能，逗号分隔
    expected_salary_min = db.Column(db.Integer)  # 期望薪资
    expected_salary_max = db.Column(db.Integer)
    expected_location = db.Column(db.String(100)) # 期望工作地点
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'location': self.location,
            'summary': self.summary,
            'experience_text': self.experience_text,
            'education_text': self.education_text,
            'skills': self.skills,
            'expected_salary_min': self.expected_salary_min,
            'expected_salary_max': self.expected_salary_max,
            'expected_location': self.expected_location,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Job(db.Model):
    """职位（保留）"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=True)  # 企业发布
    publisher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)    # 发布者
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(20))          # full_time, part_time, intern
    experience = db.Column(db.String(50))        # 经验要求
    education = db.Column(db.String(50))         # 学历要求
    status = db.Column(db.String(20), default='active')  # active, inactive
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    applications = db.relationship('Application', backref='job', lazy=True)
    publisher = db.relationship('User', backref='published_jobs', lazy=True)
    
    def to_dict(self, include_company=False, include_publisher=False):
        data = {
            'id': self.id,
            'company_id': self.company_id,
            'publisher_id': self.publisher_id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'location': self.location,
            'job_type': self.job_type,
            'experience': self.experience,
            'education': self.education,
            'status': self.status,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_company and self.company:
            data['company'] = self.company.to_dict()
        if include_publisher and self.publisher:
            data['publisher'] = self.publisher.to_dict()
            if not self.company:
                data['company_name'] = f"{self.publisher.school_name or ''}·内推".strip('·')
        return data


class Application(db.Model):
    """求职申请（保留）"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    hr_remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联 - job 关系通过 Job 模型的 backref 自动创建
    seeker = db.relationship('User', backref='applications', lazy=True)
    
    def to_dict(self, include_job=False, include_seeker=False):
        data = {
            'id': self.id,
            'job_id': self.job_id,
            'seeker_id': self.seeker_id,
            'status': self.status,
            'hr_remark': self.hr_remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_job and self.job:
            data['job'] = self.job.to_dict(include_company=True)
        if include_seeker and self.seeker:
            data['seeker'] = self.seeker.to_dict()
            if self.seeker.job_seeker_profile:
                data['seeker_profile'] = self.seeker.job_seeker_profile.to_dict()
        return data


# 【扩展】面试经验分享
class InterviewExperience(db.Model):
    __tablename__ = 'interview_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100))
    experience_type = db.Column(db.String(20), default='interview')  # interview, written_test
    content = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer)           # 难度 1-5
    result = db.Column(db.String(20))            # offer, rejected, pending
    helpful_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    is_anonymous = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='approved')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='interview_experiences', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'company_name': self.company_name,
            'job_title': self.job_title,
            'experience_type': self.experience_type,
            'content': self.content,
            'difficulty': self.difficulty,
            'result': self.result,
            'helpful_count': self.helpful_count,
            'view_count': self.view_count,
            'is_anonymous': self.is_anonymous,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_user and self.user and not self.is_anonymous:
            data['user'] = self.user.to_dict()
        return data


# 【扩展】校园宣讲会
class CampusTalk(db.Model):
    __tablename__ = 'campus_talks'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    school_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    description = db.Column(db.Text)
    registration_url = db.Column(db.String(500))
    view_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, ongoing, ended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    company = db.relationship('Company', backref='campus_talks', lazy=True)
    
    def to_dict(self, include_company=False):
        data = {
            'id': self.id,
            'title': self.title,
            'school_name': self.school_name,
            'location': self.location,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'description': self.description,
            'registration_url': self.registration_url,
            'view_count': self.view_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_company and self.company:
            data['company'] = self.company.to_dict()
        return data


# ==========================================
# 培训学习模块（全新）
# ==========================================

class TrainingCourse(db.Model):
    """培训课程"""
    __tablename__ = 'training_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    # categories: programming, language, exam_prep, career, hobby, design, data
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # 课程创建者
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
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    creator = db.relationship('User', backref='created_courses', lazy=True)
    
    def to_dict(self, include_stats=False, include_creator=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'created_by': self.created_by,
            'provider': self.provider,
            'instructor': self.instructor,
            'price': self.price,
            'original_price': self.original_price,
            'duration': self.duration,
            'level': self.level,
            'cover_image': self.cover_image,
            'detail_url': self.detail_url,
            'is_online': self.is_online,
            'location': self.location,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_stats:
            data['enrolled_count'] = self.enrolled_count
            data['rating'] = self.rating
            data['review_count'] = self.review_count
        if include_creator and self.creator:
            data['creator'] = self.creator.to_dict()
        return data


class CourseEnrollment(db.Model):
    """课程报名记录"""
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('training_courses.id'), nullable=False)
    status = db.Column(db.String(20), default='enrolled')  # enrolled, completed, dropped
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    review_content = db.Column(db.Text)
    review_rating = db.Column(db.Integer)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_enrollment'),)
    
    user = db.relationship('User', backref='course_enrollments', lazy=True)
    course = db.relationship('TrainingCourse', backref='enrollments', lazy=True)
    
    def to_dict(self, include_course=False):
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'status': self.status,
            'enrolled_at': self.enrolled_at.isoformat() if self.enrolled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'review_rating': self.review_rating
        }
        if include_course and self.course:
            data['course'] = self.course.to_dict()
        return data


class StudyMaterial(db.Model):
    """学习资料分享"""
    __tablename__ = 'study_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))          # 资料分类
    file_url = db.Column(db.String(500))
    file_type = db.Column(db.String(20))         # pdf, video, doc, etc.
    file_size = db.Column(db.String(20))
    download_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='active')  # active, removed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='study_materials', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'file_url': self.file_url,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'download_count': self.download_count,
            'like_count': self.like_count,
            'is_public': self.is_public,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


class CertificationInfo(db.Model):
    """考证信息"""
    __tablename__ = 'certification_infos'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    organizer = db.Column(db.String(100))
    registration_start = db.Column(db.Date)
    registration_end = db.Column(db.Date)
    exam_date = db.Column(db.Date)
    registration_url = db.Column(db.String(500))
    fee = db.Column(db.Float)
    requirements = db.Column(db.Text)
    status = db.Column(db.String(20), default='upcoming')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'organizer': self.organizer,
            'registration_start': self.registration_start.isoformat() if self.registration_start else None,
            'registration_end': self.registration_end.isoformat() if self.registration_end else None,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None,
            'registration_url': self.registration_url,
            'fee': self.fee,
            'requirements': self.requirements,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# ==========================================
# 社交交友模块（全新）
# ==========================================

class SocialPost(db.Model):
    """帖子/动态"""
    __tablename__ = 'social_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    post_type = db.Column(db.String(20), default='text')
    # types: text, image, video, poll, article, link
    
    images = db.Column(db.Text)                  # 图片URL列表，JSON格式
    
    # 圈子关联
    circle_id = db.Column(db.Integer, db.ForeignKey('social_circles.id'))
    
    # 话题标签
    tags = db.Column(db.String(500))             # 逗号分隔的标签
    
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
    
    user = db.relationship('User', backref='posts', lazy=True)
    circle = db.relationship('SocialCircle', backref='posts', lazy=True)
    
    def to_dict(self, include_user=False, include_circle=False):
        data = {
            'id': self.id,
            'content': self.content,
            'post_type': self.post_type,
            'images': self.images,  # JSON字符串，前端解析
            'tags': self.tags,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count,
            'view_count': self.view_count,
            'is_anonymous': self.is_anonymous,
            'is_pinned': self.is_pinned,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_user and self.user and not self.is_anonymous:
            data['user'] = self.user.to_dict()
        if include_circle and self.circle:
            data['circle'] = self.circle.to_dict()
        return data


class PostComment(db.Model):
    """帖子评论"""
    __tablename__ = 'post_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('social_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('post_comments.id'))  # 回复评论
    content = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    post = db.relationship('SocialPost', backref='comments', lazy=True)
    user = db.relationship('User', backref='comments', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'post_id': self.post_id,
            'parent_id': self.parent_id,
            'content': self.content,
            'like_count': self.like_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


class PostLike(db.Model):
    """点赞记录"""
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(20), nullable=False)  # post, comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'target_id', 'target_type', name='unique_like'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_id': self.target_id,
            'target_type': self.target_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class SocialCircle(db.Model):
    """兴趣圈子"""
    __tablename__ = 'social_circles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))          # 圈子分类
    # categories: study, career, hobby, campus, city, game, sport
    
    icon_url = db.Column(db.String(500))
    cover_url = db.Column(db.String(500))
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    member_count = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)
    
    is_public = db.Column(db.Boolean, default=True)
    need_approval = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='created_circles', lazy=True)
    
    def to_dict(self, include_creator=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'icon_url': self.icon_url,
            'cover_url': self.cover_url,
            'member_count': self.member_count,
            'topic_count': len(self.topics) if hasattr(self, 'topics') else 0,
            'is_public': self.is_public,
            'need_approval': self.need_approval,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_creator and self.creator:
            data['creator'] = self.creator.to_dict()
        return data


class CircleMember(db.Model):
    """圈子成员"""
    __tablename__ = 'circle_members'
    
    id = db.Column(db.Integer, primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('social_circles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # member, admin, owner
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('circle_id', 'user_id', name='unique_circle_member'),)
    
    circle = db.relationship('SocialCircle', backref='members', lazy=True)
    user = db.relationship('User', backref='circle_memberships', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'circle_id': self.circle_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


class SocialEvent(db.Model):
    """活动/约伴"""
    __tablename__ = 'social_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))        # sports, study, dining, travel, game, party, other
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    location = db.Column(db.String(200))
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer, default=0)
    
    # 新增字段
    cover_image = db.Column(db.String(500))      # 活动封面图
    fee_type = db.Column(db.String(20), default='free')  # free, aa, fixed
    fee_amount = db.Column(db.Integer, default=0)  # 费用金额（分）
    view_count = db.Column(db.Integer, default=0)  # 浏览次数
    
    status = db.Column(db.String(20), default='open')  # open, full, ongoing, ended, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='created_events', lazy=True)
    
    def to_dict(self, include_creator=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'location': self.location,
            'location_lat': self.location_lat,
            'location_lng': self.location_lng,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'cover_image': self.cover_image,
            'fee_type': self.fee_type,
            'fee_amount': self.fee_amount,
            'view_count': self.view_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_creator and self.creator:
            data['creator'] = self.creator.to_dict()
        return data


class EventParticipant(db.Model):
    """活动参与者"""
    __tablename__ = 'event_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('social_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='joined')  # joined, cancelled
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_event_participant'),)
    
    event = db.relationship('SocialEvent', backref='participants', lazy=True)
    user = db.relationship('User', backref='event_participations', lazy=True)


class EventComment(db.Model):
    """活动评论"""
    __tablename__ = 'event_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('social_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('event_comments.id'))  # 楼中楼回复
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    event = db.relationship('SocialEvent', backref='comments', lazy=True)
    user = db.relationship('User', backref='event_comments', lazy=True)
    parent = db.relationship('EventComment', remote_side=[id], backref='replies', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


class EventCheckIn(db.Model):
    """活动签到"""
    __tablename__ = 'event_checkins'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('social_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    checked_in_at = db.Column(db.DateTime, default=datetime.utcnow)
    check_in_method = db.Column(db.String(20), default='manual')  # manual, qrcode
    
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_event_checkin'),)
    
    event = db.relationship('SocialEvent', backref='checkins', lazy=True)
    user = db.relationship('User', backref='event_checkins', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'checked_in_at': self.checked_in_at.isoformat() if self.checked_in_at else None,
            'check_in_method': self.check_in_method
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


class EventReview(db.Model):
    """活动评价"""
    __tablename__ = 'event_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('social_events.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5星
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('event_id', 'reviewer_id', 'reviewee_id', name='unique_event_review'),)
    
    event = db.relationship('SocialEvent', backref='reviews', lazy=True)
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviews_given', lazy=True)
    reviewee = db.relationship('User', foreign_keys=[reviewee_id], backref='reviews_received', lazy=True)
    
    def to_dict(self, include_users=False):
        data = {
            'id': self.id,
            'event_id': self.event_id,
            'reviewer_id': self.reviewer_id,
            'reviewee_id': self.reviewee_id,
            'rating': self.rating,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_users:
            if self.reviewer:
                data['reviewer'] = self.reviewer.to_dict()
            if self.reviewee:
                data['reviewee'] = self.reviewee.to_dict()
        return data


class PrivateMessage(db.Model):
    """私信/聊天"""
    __tablename__ = 'private_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, image
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages', lazy=True)
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages', lazy=True)
    
    def to_dict(self, include_sender=False):
        data = {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'content': self.content,
            'message_type': self.message_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_sender and self.sender:
            data['sender'] = self.sender.to_dict()
        return data


# ==========================================
# 跳蚤市场模块（全新）
# ==========================================

class FleaItem(db.Model):
    """二手物品"""
    __tablename__ = 'flea_items'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    # categories: book, electronics, bike, dorm, ticket, clothing, other
    
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    
    condition = db.Column(db.String(20))         # new, like_new, good, fair, worn
    
    images = db.Column(db.Text)                  # 图片URL列表，JSON格式
    
    # 交易信息
    trade_location = db.Column(db.String(200))
    trade_method = db.Column(db.String(50))      # face_to_face, campus_delivery, express
    
    view_count = db.Column(db.Integer, default=0)
    favorite_count = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(20), default='on_sale')  # on_sale, reserved, sold, removed
    
    is_bargain_allowed = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sold_at = db.Column(db.DateTime)
    
    seller = db.relationship('User', backref='flea_items', lazy=True)
    
    def to_dict(self, include_seller=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'original_price': self.original_price,
            'condition': self.condition,
            'images': self.images,
            'trade_location': self.trade_location,
            'trade_method': self.trade_method,
            'view_count': self.view_count,
            'favorite_count': self.favorite_count,
            'status': self.status,
            'is_bargain_allowed': self.is_bargain_allowed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_seller and self.seller:
            data['seller'] = self.seller.to_dict()
        return data


class FleaWanted(db.Model):
    """求购信息"""
    __tablename__ = 'flea_wanted'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    max_price = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, fulfilled, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='flea_wanteds', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'max_price': self.max_price,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


# ==========================================
# 兴趣圈子话题模块
# ==========================================

class Topic(db.Model):
    """兴趣话题/帖子"""
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    tags = db.Column(db.JSON)  # 标签数组 ["求职", "内推"]
    
    visibility = db.Column(db.String(20), default='public')  # public(全站)/school_only(仅本校)
    status = db.Column(db.String(20), default='open')  # open(开放)/closed(已关闭)/solved(已解决)
    
    is_pinned = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    reply_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    last_reply_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    user = db.relationship('User', backref='topics', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags or [],
            'visibility': self.visibility,
            'status': self.status,
            'is_pinned': self.is_pinned,
            'view_count': self.view_count,
            'reply_count': self.reply_count,
            'like_count': self.like_count,
            'last_reply_at': self.last_reply_at.isoformat() if self.last_reply_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data


class TopicReply(db.Model):
    """话题回复"""
    __tablename__ = 'topic_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('topic_replies.id'))  # 楼中楼
    
    content = db.Column(db.Text, nullable=False)
    is_accepted = db.Column(db.Boolean, default=False)  # 是否被采纳为最佳答案
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    topic = db.relationship('Topic', backref='replies', lazy=True)
    user = db.relationship('User', backref='replies', lazy=True)
    parent = db.relationship('TopicReply', remote_side=[id], backref='children', lazy=True)
    
    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'topic_id': self.topic_id,
            'user_id': self.user_id,
            'parent_id': self.parent_id,
            'content': self.content,
            'is_accepted': self.is_accepted,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_user and self.user:
            data['user'] = self.user.to_dict()
        return data
