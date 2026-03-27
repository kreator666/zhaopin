from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, JobSeekerProfile, User

resumes_bp = Blueprint('resumes', __name__)

@resumes_bp.route('', methods=['GET'])
@jwt_required()
def get_resume():
    """获取我的简历"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'job_seeker':
        return jsonify({'error': '只有求职者才能查看简历'}), 403
    
    profile = user.job_seeker_profile
    if not profile:
        # 创建空简历
        profile = JobSeekerProfile(user_id=user_id, name=user.username)
        db.session.add(profile)
        db.session.commit()
    
    return jsonify(profile.to_dict())


@resumes_bp.route('', methods=['POST'])
@jwt_required()
def create_or_update_resume():
    """创建或更新简历"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'job_seeker':
        return jsonify({'error': '只有求职者才能编辑简历'}), 403
    
    data = request.get_json()
    
    profile = user.job_seeker_profile
    if not profile:
        profile = JobSeekerProfile(user_id=user_id)
    
    # 更新字段
    profile.name = data.get('name', profile.name)
    profile.gender = data.get('gender', profile.gender)
    profile.birth_date = data.get('birth_date') or profile.birth_date
    profile.location = data.get('location', profile.location)
    profile.summary = data.get('summary', profile.summary)
    profile.experience_text = data.get('experience_text', profile.experience_text)
    profile.education_text = data.get('education_text', profile.education_text)
    profile.skills = data.get('skills', profile.skills)
    
    db.session.add(profile)
    db.session.commit()
    
    return jsonify({
        'message': '简历保存成功',
        'profile': profile.to_dict()
    })


@resumes_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_resume_by_user(user_id):
    """获取指定用户的简历（用于HR查看）"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.role != 'company':
        return jsonify({'error': '无权查看'}), 403
    
    profile = JobSeekerProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({'error': '简历不存在'}), 404
    
    return jsonify(profile.to_dict())
