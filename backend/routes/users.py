"""
用户管理路由
- 用户资料
- 关注/粉丝
- 用户动态
- 技能认证
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, UserFollow, UserActivity, UserSkill, UserBadge

users_bp = Blueprint('users', __name__)


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    """获取用户资料（包含完整关联数据）"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict(
        include_profile=True,
        include_skills=True,
        include_badges=True
    ))


@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    """获取当前用户资料（包含完整关联数据）"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict(
        include_profile=True,
        include_skills=True,
        include_badges=True
    ))


@users_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新个人资料"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # 可更新的字段
    allowed_fields = [
        'username', 'phone', 'school_name', 'major',
        'enrollment_year', 'graduation_year', 'bio',
        'avatar_url', 'cover_url', 'is_public'
    ]
    
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    db.session.commit()
    return jsonify({'message': '资料更新成功', 'user': user.to_dict()})


@users_bp.route('/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    """关注用户"""
    current_user_id = get_jwt_identity()
    
    if current_user_id == user_id:
        return jsonify({'error': '不能关注自己'}), 400
    
    # 检查是否已关注
    existing = UserFollow.query.filter_by(
        follower_id=current_user_id,
        following_id=user_id
    ).first()
    
    if existing:
        return jsonify({'error': '已关注该用户'}), 400
    
    # 创建关注关系
    follow = UserFollow(follower_id=current_user_id, following_id=user_id)
    db.session.add(follow)
    
    # 更新计数
    current_user = User.query.get(current_user_id)
    target_user = User.query.get(user_id)
    current_user.following_count = (current_user.following_count or 0) + 1
    target_user.follower_count = (target_user.follower_count or 0) + 1
    
    # 创建动态记录
    activity = UserActivity(
        user_id=current_user_id,
        activity_type='follow',
        target_id=user_id,
        target_type='user',
        content=f'关注了 {target_user.username}'
    )
    db.session.add(activity)
    
    db.session.commit()
    return jsonify({'message': '关注成功'})


@users_bp.route('/<int:user_id>/follow', methods=['DELETE'])
@jwt_required()
def unfollow_user(user_id):
    """取消关注"""
    current_user_id = get_jwt_identity()
    
    follow = UserFollow.query.filter_by(
        follower_id=current_user_id,
        following_id=user_id
    ).first()
    
    if not follow:
        return jsonify({'error': '未关注该用户'}), 400
    
    db.session.delete(follow)
    
    # 更新计数
    current_user = User.query.get(current_user_id)
    target_user = User.query.get(user_id)
    current_user.following_count -= 1
    target_user.follower_count -= 1
    
    db.session.commit()
    return jsonify({'message': '取消关注成功'})


@users_bp.route('/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    """获取粉丝列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    followers = UserFollow.query.filter_by(following_id=user_id)\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [f.follower.to_dict() for f in followers.items],
        'total': followers.total,
        'pages': followers.pages,
        'current_page': page
    })


@users_bp.route('/<int:user_id>/following', methods=['GET'])
def get_following(user_id):
    """获取关注列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    following = UserFollow.query.filter_by(follower_id=user_id)\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [f.following.to_dict() for f in following.items],
        'total': following.total,
        'pages': following.pages,
        'current_page': page
    })


@users_bp.route('/<int:user_id>/activities', methods=['GET'])
def get_user_activities(user_id):
    """获取用户动态"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    activities = UserActivity.query.filter_by(user_id=user_id)\
        .order_by(UserActivity.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [a.to_dict() for a in activities.items],
        'total': activities.total,
        'pages': activities.pages,
        'current_page': page
    })


@users_bp.route('/me/skills', methods=['POST'])
@jwt_required()
def add_skill():
    """添加技能"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    skill = UserSkill(
        user_id=user_id,
        skill_name=data.get('skill_name'),
        proficiency=data.get('proficiency', 3),
        certification=data.get('certification')
    )
    db.session.add(skill)
    db.session.commit()
    
    return jsonify({'message': '技能添加成功', 'skill': skill.to_dict()})


@users_bp.route('/me/skills/<int:skill_id>', methods=['DELETE'])
@jwt_required()
def delete_skill(skill_id):
    """删除技能"""
    user_id = get_jwt_identity()
    skill = UserSkill.query.filter_by(id=skill_id, user_id=user_id).first_or_404()
    db.session.delete(skill)
    db.session.commit()
    return jsonify({'message': '技能删除成功'})


@users_bp.route('/search', methods=['GET'])
def search_users():
    """搜索用户"""
    keyword = request.args.get('q', '')
    school = request.args.get('school', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = User.query
    
    if keyword:
        query = query.filter(
            db.or_(
                User.username.contains(keyword),
                User.bio.contains(keyword)
            )
        )
    
    if school:
        query = query.filter(User.school_name.contains(school))
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [u.to_dict() for u in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    })
