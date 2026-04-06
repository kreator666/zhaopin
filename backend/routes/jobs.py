from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Job, Company, User

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('', methods=['GET'])
def get_jobs():
    """获取职位列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    
    query = Job.query.filter_by(status='active')
    
    # 关键词搜索
    if keyword:
        query = query.filter(
            db.or_(
                Job.title.contains(keyword),
                Job.description.contains(keyword)
            )
        )
    
    # 地点筛选
    if location:
        query = query.filter(Job.location.contains(location))
    
    # 按时间倒序
    query = query.order_by(Job.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [job.to_dict(include_company=True) for job in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """获取职位详情"""
    job = Job.query.get_or_404(job_id)
    
    # 增加浏览量
    job.view_count += 1
    db.session.commit()
    
    return jsonify(job.to_dict(include_company=True))


@jobs_bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    """发布职位（企业用户或认证学生/校友）"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 企业用户必须有公司信息
    if user.role == 'company' and not user.company:
        return jsonify({'error': '请先完善企业信息'}), 400
    
    # 学生/校友需要学校认证
    if user.role in ('student', 'alumni', 'job_seeker'):
        if not user.student_verified and not user.school_name:
            return jsonify({'error': '请先完善学校信息'}), 400
    elif user.role != 'company':
        return jsonify({'error': '无权发布职位'}), 403
    
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['title', 'description']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    job = Job(
        company_id=user.company.id if user.role == 'company' else None,
        publisher_id=user.id,
        title=data['title'],
        description=data['description'],
        requirements=data.get('requirements', ''),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        location=data.get('location', ''),
        job_type=data.get('job_type', 'full_time'),
        experience=data.get('experience', ''),
        education=data.get('education', '')
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'message': '职位发布成功',
        'job': job.to_dict()
    }), 201


@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """更新职位"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    job = Job.query.get_or_404(job_id)
    
    # 检查权限
    if user.role != 'company' or job.company_id != user.company.id:
        return jsonify({'error': '无权修改此职位'}), 403
    
    data = request.get_json()
    
    # 更新字段
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.requirements = data.get('requirements', job.requirements)
    job.salary_min = data.get('salary_min', job.salary_min)
    job.salary_max = data.get('salary_max', job.salary_max)
    job.location = data.get('location', job.location)
    job.job_type = data.get('job_type', job.job_type)
    job.experience = data.get('experience', job.experience)
    job.education = data.get('education', job.education)
    job.status = data.get('status', job.status)
    
    db.session.commit()
    
    return jsonify({
        'message': '职位更新成功',
        'job': job.to_dict()
    })


@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """删除职位"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    job = Job.query.get_or_404(job_id)
    
    # 检查权限
    if user.role != 'company' or job.company_id != user.company.id:
        return jsonify({'error': '无权删除此职位'}), 403
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'message': '职位删除成功'})


@jobs_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_jobs():
    """获取我发布的职位（企业用户）"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'company':
        return jsonify({'error': '只有企业用户才能查看'}), 403
    
    if not user.company:
        return jsonify({'items': [], 'total': 0})
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Job.query.filter_by(company_id=user.company.id)\
        .order_by(Job.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [job.to_dict() for job in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })
