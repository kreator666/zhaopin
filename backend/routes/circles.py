"""
兴趣圈子路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, SocialCircle, CircleMember

circles_bp = Blueprint('circles', __name__)


@circles_bp.route('', methods=['GET'])
def get_circles():
    """获取圈子列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    
    query = SocialCircle.query.filter_by(is_public=True)
    
    if category:
        query = query.filter_by(category=category)
    
    circles = query.order_by(SocialCircle.member_count.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [c.to_dict(include_creator=True) for c in circles.items],
        'total': circles.total,
        'pages': circles.pages,
        'current_page': page
    })


@circles_bp.route('/<int:circle_id>', methods=['GET'])
def get_circle(circle_id):
    """获取圈子详情"""
    circle = SocialCircle.query.get_or_404(circle_id)
    return jsonify(circle.to_dict(include_creator=True))


@circles_bp.route('', methods=['POST'])
@jwt_required()
def create_circle():
    """创建圈子"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    circle = SocialCircle(
        name=data.get('name'),
        description=data.get('description'),
        category=data.get('category'),
        icon_url=data.get('icon_url'),
        cover_url=data.get('cover_url'),
        creator_id=user_id,
        is_public=data.get('is_public', True),
        need_approval=data.get('need_approval', False)
    )
    db.session.add(circle)
    db.session.flush()  # 获取 circle.id
    
    # 创建者自动成为管理员
    member = CircleMember(
        circle_id=circle.id,
        user_id=user_id,
        role='owner'
    )
    db.session.add(member)
    circle.member_count = 1
    
    db.session.commit()
    return jsonify({'message': '圈子创建成功', 'circle': circle.to_dict()})


@circles_bp.route('/<int:circle_id>/join', methods=['POST'])
@jwt_required()
def join_circle(circle_id):
    """加入圈子"""
    user_id = get_jwt_identity()
    circle = SocialCircle.query.get_or_404(circle_id)
    
    # 检查是否已加入
    existing = CircleMember.query.filter_by(
        circle_id=circle_id, user_id=user_id
    ).first()
    if existing:
        return jsonify({'error': '已加入该圈子'}), 400
    
    member = CircleMember(
        circle_id=circle_id,
        user_id=user_id,
        role='member'
    )
    db.session.add(member)
    circle.member_count += 1
    db.session.commit()
    
    return jsonify({'message': '加入成功'})


@circles_bp.route('/<int:circle_id>/leave', methods=['POST'])
@jwt_required()
def leave_circle(circle_id):
    """退出圈子"""
    user_id = get_jwt_identity()
    
    member = CircleMember.query.filter_by(
        circle_id=circle_id, user_id=user_id
    ).first()
    
    if not member:
        return jsonify({'error': '未加入该圈子'}), 400
    
    db.session.delete(member)
    circle = SocialCircle.query.get(circle_id)
    circle.member_count -= 1
    db.session.commit()
    
    return jsonify({'message': '退出成功'})


@circles_bp.route('/<int:circle_id>/members', methods=['GET'])
def get_circle_members(circle_id):
    """获取圈子成员"""
    members = CircleMember.query.filter_by(circle_id=circle_id).all()
    return jsonify({
        'items': [m.to_dict(include_user=True) for m in members]
    })


@circles_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_circles():
    """获取我加入的圈子"""
    user_id = get_jwt_identity()
    memberships = CircleMember.query.filter_by(user_id=user_id).all()
    
    circles = [m.circle.to_dict() for m in memberships]
    return jsonify({'items': circles})
