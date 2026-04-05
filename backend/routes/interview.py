"""
面试经验、校园宣讲会路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, InterviewExperience, CampusTalk

interview_bp = Blueprint('interview', __name__)


# ========== 面试经验 ==========

@interview_bp.route('/experiences', methods=['GET'])
def get_experiences():
    """获取面试经验列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    company = request.args.get('company', '')
    result = request.args.get('result', '')
    
    query = InterviewExperience.query.filter_by(status='approved')
    
    if company:
        query = query.filter(InterviewExperience.company_name.contains(company))
    if result:
        query = query.filter_by(result=result)
    
    experiences = query.order_by(InterviewExperience.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [e.to_dict(include_user=True) for e in experiences.items],
        'total': experiences.total,
        'pages': experiences.pages,
        'current_page': page
    })


@interview_bp.route('/experiences/<int:exp_id>', methods=['GET'])
def get_experience(exp_id):
    """获取面试经验详情"""
    exp = InterviewExperience.query.get_or_404(exp_id)
    exp.view_count += 1
    db.session.commit()
    return jsonify(exp.to_dict(include_user=True))


@interview_bp.route('/experiences', methods=['POST'])
@jwt_required()
def create_experience():
    """发布面试经验"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    exp = InterviewExperience(
        user_id=user_id,
        company_name=data.get('company_name'),
        job_title=data.get('job_title'),
        experience_type=data.get('experience_type', 'interview'),
        content=data.get('content'),
        difficulty=data.get('difficulty'),
        result=data.get('result'),
        is_anonymous=data.get('is_anonymous', False),
        status='approved'  # 实际应用中可能需要审核
    )
    db.session.add(exp)
    db.session.commit()
    
    return jsonify({'message': '发布成功', 'experience': exp.to_dict()})


@interview_bp.route('/experiences/<int:exp_id>/helpful', methods=['POST'])
@jwt_required()
def mark_helpful(exp_id):
    """标记为有帮助"""
    exp = InterviewExperience.query.get_or_404(exp_id)
    exp.helpful_count += 1
    db.session.commit()
    return jsonify({'message': '已标记为有帮助'})


# ========== 校园宣讲会 ==========

@interview_bp.route('/campus-talks', methods=['GET'])
def get_campus_talks():
    """获取宣讲会列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    school = request.args.get('school', '')
    status = request.args.get('status', '')
    
    query = CampusTalk.query
    
    if school:
        query = query.filter(CampusTalk.school_name.contains(school))
    if status:
        query = query.filter_by(status=status)
    
    talks = query.order_by(CampusTalk.start_time.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [t.to_dict(include_company=True) for t in talks.items],
        'total': talks.total,
        'pages': talks.pages,
        'current_page': page
    })


@interview_bp.route('/campus-talks/<int:talk_id>', methods=['GET'])
def get_campus_talk(talk_id):
    """获取宣讲会详情"""
    talk = CampusTalk.query.get_or_404(talk_id)
    talk.view_count += 1
    db.session.commit()
    return jsonify(talk.to_dict(include_company=True))


@interview_bp.route('/campus-talks', methods=['POST'])
@jwt_required()
def create_campus_talk():
    """企业发布宣讲会"""
    user_id = int(get_jwt_identity())
    from models import User, Company
    from datetime import datetime
    
    user = User.query.get(user_id)
    if not user or user.role != 'company':
        return jsonify({'error': '只有企业用户才能发布宣讲会'}), 403
    
    if not user.company:
        return jsonify({'error': '请先完善企业信息'}), 400
    
    data = request.get_json()
    
    # 验证必填字段
    required = ['title', 'school_name', 'start_time']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 解析日期时间
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time']) if data.get('end_time') else None
    except ValueError as e:
        return jsonify({'error': f'日期格式错误: {str(e)}'}), 400
    
    talk = CampusTalk(
        company_id=user.company.id,
        title=data['title'],
        school_name=data['school_name'],
        location=data.get('location', ''),
        start_time=start_time,
        end_time=end_time,
        description=data.get('description', ''),
        registration_url=data.get('registration_url', ''),
        status='upcoming'
    )
    
    db.session.add(talk)
    db.session.commit()
    
    return jsonify({
        'message': '宣讲会发布成功',
        'talk': talk.to_dict()
    }), 201


@interview_bp.route('/campus-talks/<int:talk_id>', methods=['PUT'])
@jwt_required()
def update_campus_talk(talk_id):
    """企业更新宣讲会"""
    user_id = int(get_jwt_identity())
    from models import User
    from datetime import datetime
    
    user = User.query.get(user_id)
    talk = CampusTalk.query.get_or_404(talk_id)
    
    # 检查权限
    if user.role != 'company' or talk.company_id != user.company.id:
        return jsonify({'error': '无权修改此宣讲会'}), 403
    
    data = request.get_json()
    
    talk.title = data.get('title', talk.title)
    talk.school_name = data.get('school_name', talk.school_name)
    talk.location = data.get('location', talk.location)
    
    # 解析日期时间
    if 'start_time' in data and data['start_time']:
        try:
            talk.start_time = datetime.fromisoformat(data['start_time'])
        except ValueError as e:
            return jsonify({'error': f'开始时间格式错误: {str(e)}'}), 400
    
    if 'end_time' in data and data['end_time']:
        try:
            talk.end_time = datetime.fromisoformat(data['end_time'])
        except ValueError as e:
            return jsonify({'error': f'结束时间格式错误: {str(e)}'}), 400
    
    talk.description = data.get('description', talk.description)
    talk.registration_url = data.get('registration_url', talk.registration_url)
    
    db.session.commit()
    
    return jsonify({
        'message': '更新成功',
        'talk': talk.to_dict()
    })


@interview_bp.route('/campus-talks/<int:talk_id>', methods=['DELETE'])
@jwt_required()
def delete_campus_talk(talk_id):
    """企业删除宣讲会"""
    user_id = int(get_jwt_identity())
    from models import User
    
    user = User.query.get(user_id)
    talk = CampusTalk.query.get_or_404(talk_id)
    
    # 检查权限
    if user.role != 'company' or talk.company_id != user.company_id:
        return jsonify({'error': '无权删除此宣讲会'}), 403
    
    db.session.delete(talk)
    db.session.commit()
    
    return jsonify({'message': '删除成功'})


@interview_bp.route('/my/campus-talks', methods=['GET'])
@jwt_required()
def get_my_campus_talks():
    """获取当前企业的宣讲会列表"""
    user_id = int(get_jwt_identity())
    from models import User
    
    user = User.query.get(user_id)
    if not user or user.role != 'company':
        return jsonify({'error': '只有企业用户才能查看'}), 403
    
    if not user.company:
        return jsonify({'items': [], 'total': 0})
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    talks = CampusTalk.query.filter_by(company_id=user.company.id)\
        .order_by(CampusTalk.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [t.to_dict() for t in talks.items],
        'total': talks.total,
        'pages': talks.pages,
        'current_page': page
    })
