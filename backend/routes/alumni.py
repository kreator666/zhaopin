"""
校友圈路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

alumni_bp = Blueprint('alumni', __name__)


@alumni_bp.route('/circle', methods=['GET'])
@jwt_required()
def get_alumni_circle():
    """获取校友圈 - 同一学校的用户列表"""
    user_id = int(get_jwt_identity())
    current_user = User.query.get(user_id)
    
    if not current_user or not current_user.school_name:
        return jsonify({'error': '请先完善学校信息'}), 400
    
    # 搜索参数
    keyword = request.args.get('keyword', '')
    gender = request.args.get('gender', '')
    enrollment_year = request.args.get('enrollment_year', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 基础查询 - 同一学校，排除自己
    query = User.query.filter(
        User.school_name == current_user.school_name,
        User.id != user_id
    )
    
    # 按名字搜索
    if keyword:
        query = query.filter(User.username.ilike(f'%{keyword}%'))
    
    # 按性别筛选
    if gender:
        query = query.filter(User.gender == gender)
    
    # 按入学年份筛选
    if enrollment_year:
        query = query.filter(User.enrollment_year == enrollment_year)
    
    # 分页
    pagination = query.order_by(User.enrollment_year.desc(), User.username.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'school_name': current_user.school_name
    })


@alumni_bp.route('/years', methods=['GET'])
@jwt_required()
def get_alumni_years():
    """获取校友圈所有入学年份（用于筛选）"""
    user_id = int(get_jwt_identity())
    current_user = User.query.get(user_id)
    
    if not current_user or not current_user.school_name:
        return jsonify({'items': []})
    
    # 获取该学校所有不同的入学年份
    years = db.session.query(User.enrollment_year.distinct()).filter(
        User.school_name == current_user.school_name,
        User.enrollment_year.isnot(None)
    ).order_by(User.enrollment_year.desc()).all()
    
    return jsonify({
        'items': [year[0] for year in years if year[0]]
    })


@alumni_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_alumni_stats():
    """获取校友圈统计"""
    user_id = int(get_jwt_identity())
    current_user = User.query.get(user_id)
    
    if not current_user or not current_user.school_name:
        return jsonify({'error': '请先完善学校信息'}), 400
    
    # 统计
    total_alumni = User.query.filter(
        User.school_name == current_user.school_name,
        User.id != user_id
    ).count()
    
    same_year_count = 0
    if current_user.enrollment_year:
        same_year_count = User.query.filter(
            User.school_name == current_user.school_name,
            User.enrollment_year == current_user.enrollment_year,
            User.id != user_id
        ).count()
    
    return jsonify({
        'school_name': current_user.school_name,
        'total_alumni': total_alumni,
        'same_year_count': same_year_count,
        'my_year': current_user.enrollment_year
    })
