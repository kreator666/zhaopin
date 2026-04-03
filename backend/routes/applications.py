from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Application, Job, User, UserActivity

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('', methods=['POST'])
@jwt_required()
def apply_job():
    """投递简历"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role == 'company':
        return jsonify({'error': '只有求职者才能投递简历'}), 403
    
    data = request.get_json()
    job_id = data.get('job_id')
    
    if not job_id:
        return jsonify({'error': '缺少职位ID'}), 400
    
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': '职位不存在'}), 404
    
    if job.status != 'active':
        return jsonify({'error': '该职位已停止招聘'}), 400
    
    # 检查是否已投递
    existing = Application.query.filter_by(job_id=job_id, seeker_id=user_id).first()
    if existing:
        return jsonify({'error': '您已投递过该职位'}), 400
    
    application = Application(
        job_id=job_id,
        seeker_id=user_id,
        status='pending'
    )
    
    db.session.add(application)
    
    # 创建动态记录
    activity = UserActivity(
        user_id=user_id,
        activity_type='job_apply',
        target_id=job_id,
        target_type='job',
        content=f'投递了职位「{job.title}」'
    )
    db.session.add(activity)
    
    # 更新用户动态计数
    user.post_count = (user.post_count or 0) + 1
    
    db.session.commit()
    
    return jsonify({
        'message': '投递成功',
        'application': application.to_dict(include_job=True)
    }), 201


@applications_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_applications():
    """获取我的投递记录（求职者）"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role == 'company':
        return jsonify({'error': '只有求职者才能查看'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Application.query.filter_by(seeker_id=user_id)\
        .order_by(Application.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [app.to_dict(include_job=True) for app in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@applications_bp.route('/received', methods=['GET'])
@jwt_required()
def get_received_applications():
    """获取收到的简历（企业HR）"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'company':
        return jsonify({'error': '只有企业用户才能查看'}), 403
    
    if not user.company:
        return jsonify({'items': [], 'total': 0})
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 获取该企业所有职位的投递
    job_ids = [job.id for job in user.company.jobs]
    
    pagination = Application.query.filter(Application.job_id.in_(job_ids))\
        .order_by(Application.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [app.to_dict(include_job=True, include_seeker=True) for app in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@applications_bp.route('/<int:app_id>', methods=['PUT'])
@jwt_required()
def update_application(app_id):
    """更新投递状态（企业HR接受/拒绝）"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'company':
        return jsonify({'error': '无权操作'}), 403
    
    application = Application.query.get_or_404(app_id)
    job = Job.query.get(application.job_id)
    
    # 检查是否是该企业的职位
    if job.company_id != user.company.id:
        return jsonify({'error': '无权操作此投递'}), 403
    
    data = request.get_json()
    
    if 'status' in data:
        if data['status'] not in ['pending', 'accepted', 'rejected']:
            return jsonify({'error': '无效的状态'}), 400
        application.status = data['status']
    
    if 'hr_remark' in data:
        application.hr_remark = data['hr_remark']
    
    db.session.commit()
    
    return jsonify({
        'message': '状态更新成功',
        'application': application.to_dict(include_job=True, include_seeker=True)
    })
