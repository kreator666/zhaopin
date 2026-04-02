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
