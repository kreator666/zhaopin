from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Company, JobSeekerProfile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证必填字段
    if not all(k in data for k in ('username', 'email', 'password', 'role')):
        return jsonify({'error': '缺少必填字段'}), 400
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已被注册'}), 400
    
    # 创建用户
    user = User(
        username=data['username'],
        email=data['email'],
        role=data['role'],
        phone=data.get('phone')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.flush()  # 获取user.id
    
    # 根据角色创建关联数据
    if data['role'] == 'company':
        if not data.get('company_name'):
            db.session.rollback()
            return jsonify({'error': '企业用户必须提供公司名称'}), 400
        company = Company(
            user_id=user.id,
            name=data['company_name'],
            description=data.get('company_description', ''),
            location=data.get('company_location', ''),
            industry=data.get('industry', '')
        )
        db.session.add(company)
    else:
        # 求职者默认创建空简历
        profile = JobSeekerProfile(user_id=user.id, name=data['username'])
        db.session.add(profile)
    
    db.session.commit()
    
    # 生成token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': '注册成功',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': '请提供用户名和密码'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': '登录成功',
        'access_token': access_token,
        'user': user.to_dict()
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    result = user.to_dict()
    
    # 根据角色返回额外信息
    if user.role == 'company' and user.company:
        result['company'] = user.company.to_dict()
    elif user.role == 'job_seeker' and user.job_seeker_profile:
        result['profile'] = user.job_seeker_profile.to_dict()
    
    return jsonify(result)
