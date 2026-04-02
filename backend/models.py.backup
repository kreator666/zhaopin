from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='job_seeker')  # job_seeker, company
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    company = db.relationship('Company', backref='user', uselist=False)
    job_seeker_profile = db.relationship('JobSeekerProfile', backref='user', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    scale = db.Column(db.String(50))  # 公司规模
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
    __tablename__ = 'job_seeker_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    birth_date = db.Column(db.Date)
    location = db.Column(db.String(100))
    summary = db.Column(db.Text)  # 个人简介
    experience_text = db.Column(db.Text)  # 工作经历（简化版）
    education_text = db.Column(db.Text)  # 教育经历（简化版）
    skills = db.Column(db.String(500))  # 技能，逗号分隔
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
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(20))  # full_time, part_time, intern
    experience = db.Column(db.String(50))  # 经验要求
    education = db.Column(db.String(50))  # 学历要求
    status = db.Column(db.String(20), default='active')  # active, inactive
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    applications = db.relationship('Application', backref='job', lazy=True)
    
    def to_dict(self, include_company=False):
        data = {
            'id': self.id,
            'company_id': self.company_id,
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
        return data


class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    hr_remark = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    seeker = db.relationship('User', backref='applications')
    
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
