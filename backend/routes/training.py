"""
培训学习模块路由
- 课程
- 学习资料
- 考证信息
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from models import db, User, TrainingCourse, CourseEnrollment, StudyMaterial, CertificationInfo

training_bp = Blueprint('training', __name__)


def get_current_user():
    """获取当前登录用户"""
    user_id = int(get_jwt_identity())
    return User.query.get(user_id)


def is_admin_or_company(user):
    """检查用户是否是管理员或企业用户"""
    if not user:
        return False
    return user.role in ['admin', 'company']


def can_edit_course(user, course):
    """检查用户是否可以编辑课程"""
    if not user:
        return False
    # 管理员可以编辑所有课程
    if user.role == 'admin':
        return True
    # 企业用户只能编辑自己创建的课程
    if user.role == 'company' and course.created_by == user.id:
        return True
    return False


# ========== 课程（学生端）==========

@training_bp.route('/courses', methods=['GET'])
def get_courses():
    """获取课程列表（学生端）"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    level = request.args.get('level', '')
    is_online = request.args.get('is_online', '')
    keyword = request.args.get('keyword', '')
    
    query = TrainingCourse.query.filter_by(status='active')
    
    if category:
        query = query.filter_by(category=category)
    if level:
        query = query.filter_by(level=level)
    if is_online:
        query = query.filter_by(is_online=is_online.lower() == 'true')
    if keyword:
        keyword_pattern = f'%{keyword}%'
        query = query.filter(
            or_(
                TrainingCourse.title.like(keyword_pattern),
                TrainingCourse.description.like(keyword_pattern),
                TrainingCourse.provider.like(keyword_pattern),
                TrainingCourse.instructor.like(keyword_pattern)
            )
        )
    
    courses = query.order_by(TrainingCourse.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [c.to_dict(include_stats=True) for c in courses.items],
        'total': courses.total,
        'pages': courses.pages,
        'current_page': page
    })


@training_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """获取课程详情（学生端）"""
    course = TrainingCourse.query.get_or_404(course_id)
    return jsonify(course.to_dict(include_stats=True, include_creator=True))


@training_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_course(course_id):
    """报名课程（学生端）"""
    user_id = int(get_jwt_identity())
    course = TrainingCourse.query.get_or_404(course_id)
    
    if course.status != 'active':
        return jsonify({'error': '课程不可报名'}), 400
    
    # 检查是否已报名
    existing = CourseEnrollment.query.filter_by(
        user_id=user_id, course_id=course_id
    ).first()
    if existing:
        return jsonify({'error': '已报名该课程'}), 400
    
    enrollment = CourseEnrollment(user_id=user_id, course_id=course_id)
    course.enrolled_count += 1
    db.session.add(enrollment)
    db.session.commit()
    
    return jsonify({'message': '报名成功'})


@training_bp.route('/courses/<int:course_id>/check-enrollment', methods=['GET'])
@jwt_required()
def check_enrollment(course_id):
    """检查是否已报名"""
    user_id = int(get_jwt_identity())
    existing = CourseEnrollment.query.filter_by(
        user_id=user_id, course_id=course_id
    ).first()
    return jsonify({'enrolled': existing is not None})


@training_bp.route('/my-courses', methods=['GET'])
@jwt_required()
def get_my_courses():
    """获取我的报名课程（学生端）"""
    user_id = int(get_jwt_identity())
    status = request.args.get('status', '')
    
    query = CourseEnrollment.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    enrollments = query.order_by(CourseEnrollment.enrolled_at.desc()).all()
    return jsonify({
        'items': [e.to_dict(include_course=True) for e in enrollments]
    })


# ========== 课程（运营端：管理员/企业用户）==========

@training_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    """创建课程（运营端）"""
    user = get_current_user()
    if not is_admin_or_company(user):
        return jsonify({'error': '无权创建课程'}), 403
    
    data = request.get_json()
    
    if not data.get('title') or not data.get('category'):
        return jsonify({'error': '缺少必要字段'}), 400
    
    # 解析日期
    start_date = None
    if data.get('start_date'):
        try:
            start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        except ValueError:
            pass
    
    end_date = None
    if data.get('end_date'):
        try:
            end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # 获取提供方名称
    provider = data.get('provider')
    if not provider and user.role == 'company' and user.company:
        provider = user.company.name
    
    course = TrainingCourse(
        title=data.get('title'),
        description=data.get('description', ''),
        category=data.get('category'),
        created_by=user.id,
        provider=provider,
        instructor=data.get('instructor'),
        price=data.get('price', 0),
        original_price=data.get('original_price'),
        duration=data.get('duration'),
        level=data.get('level', 'beginner'),
        cover_image=data.get('cover_image'),
        detail_url=data.get('detail_url'),
        is_online=data.get('is_online', True),
        location=data.get('location'),
        start_date=start_date,
        end_date=end_date,
        status=data.get('status', 'active')
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify({
        'message': '创建成功',
        'course': course.to_dict(include_stats=True)
    }), 201


@training_bp.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    """更新课程（运营端）"""
    user = get_current_user()
    course = TrainingCourse.query.get_or_404(course_id)
    
    if not can_edit_course(user, course):
        return jsonify({'error': '无权修改该课程'}), 403
    
    data = request.get_json()
    
    if data.get('title'):
        course.title = data.get('title')
    if data.get('description') is not None:
        course.description = data.get('description')
    if data.get('category'):
        course.category = data.get('category')
    if data.get('provider'):
        course.provider = data.get('provider')
    if data.get('instructor'):
        course.instructor = data.get('instructor')
    if data.get('price') is not None:
        course.price = data.get('price')
    if data.get('original_price') is not None:
        course.original_price = data.get('original_price')
    if data.get('duration'):
        course.duration = data.get('duration')
    if data.get('level'):
        course.level = data.get('level')
    if data.get('cover_image'):
        course.cover_image = data.get('cover_image')
    if data.get('detail_url'):
        course.detail_url = data.get('detail_url')
    if data.get('is_online') is not None:
        course.is_online = data.get('is_online')
    if data.get('location'):
        course.location = data.get('location')
    if data.get('status'):
        course.status = data.get('status')
    
    # 解析日期
    if data.get('start_date'):
        try:
            course.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        except ValueError:
            pass
    if data.get('end_date'):
        try:
            course.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        except ValueError:
            pass
    
    db.session.commit()
    
    return jsonify({
        'message': '更新成功',
        'course': course.to_dict(include_stats=True)
    })


@training_bp.route('/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    """删除课程（运营端 - 软删除）"""
    user = get_current_user()
    course = TrainingCourse.query.get_or_404(course_id)
    
    if not can_edit_course(user, course):
        return jsonify({'error': '无权删除该课程'}), 403
    
    course.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'message': '删除成功'})


@training_bp.route('/admin/courses', methods=['GET'])
@jwt_required()
def get_admin_courses():
    """获取所有课程（运营端管理）"""
    user = get_current_user()
    if not is_admin_or_company(user):
        return jsonify({'error': '无权访问'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    category = request.args.get('category', '')
    
    query = TrainingCourse.query
    
    # 企业用户只能看到自己的课程
    if user.role == 'company':
        query = query.filter_by(created_by=user.id)
    
    if status:
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
    
    courses = query.order_by(TrainingCourse.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [c.to_dict(include_stats=True, include_creator=True) for c in courses.items],
        'total': courses.total,
        'pages': courses.pages,
        'current_page': page
    })


# ========== 学习资料 ==========

@training_bp.route('/materials', methods=['GET'])
def get_materials():
    """获取学习资料列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    
    query = StudyMaterial.query.filter_by(is_public=True, status='active')
    
    if category:
        query = query.filter_by(category=category)
    
    materials = query.order_by(StudyMaterial.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [m.to_dict(include_user=True) for m in materials.items],
        'total': materials.total,
        'pages': materials.pages,
        'current_page': page
    })


@training_bp.route('/materials', methods=['POST'])
@jwt_required()
def upload_material():
    """上传学习资料"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    material = StudyMaterial(
        user_id=user_id,
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        file_url=data.get('file_url'),
        file_type=data.get('file_type'),
        file_size=data.get('file_size'),
        is_public=data.get('is_public', True)
    )
    db.session.add(material)
    db.session.commit()
    
    return jsonify({'message': '上传成功', 'material': material.to_dict()})


@training_bp.route('/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """获取学习资料详情"""
    material = StudyMaterial.query.get_or_404(material_id)
    return jsonify(material.to_dict(include_user=True))


@training_bp.route('/materials/<int:material_id>', methods=['PUT'])
@jwt_required()
def update_material(material_id):
    """更新学习资料"""
    user_id = int(get_jwt_identity())
    material = StudyMaterial.query.get_or_404(material_id)
    
    if material.user_id != user_id:
        return jsonify({'error': '无权修改'}), 403
    
    data = request.get_json()
    
    if data.get('title'):
        material.title = data.get('title')
    if data.get('description') is not None:
        material.description = data.get('description')
    if data.get('category'):
        material.category = data.get('category')
    if data.get('file_url'):
        material.file_url = data.get('file_url')
    if data.get('file_type'):
        material.file_type = data.get('file_type')
    if data.get('file_size'):
        material.file_size = data.get('file_size')
    if data.get('is_public') is not None:
        material.is_public = data.get('is_public')
    
    db.session.commit()
    return jsonify({'message': '更新成功', 'material': material.to_dict()})


@training_bp.route('/materials/<int:material_id>', methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
    """删除学习资料"""
    user_id = int(get_jwt_identity())
    material = StudyMaterial.query.get_or_404(material_id)
    
    if material.user_id != user_id:
        return jsonify({'error': '无权删除'}), 403
    
    material.status = 'removed'
    db.session.commit()
    return jsonify({'message': '删除成功'})


@training_bp.route('/materials/<int:material_id>/download', methods=['POST'])
def download_material(material_id):
    """下载资料（计数）"""
    material = StudyMaterial.query.get_or_404(material_id)
    material.download_count += 1
    db.session.commit()
    return jsonify({'download_url': material.file_url})


@training_bp.route('/materials/<int:material_id>/like', methods=['POST'])
@jwt_required()
def like_material(material_id):
    """点赞资料"""
    material = StudyMaterial.query.get_or_404(material_id)
    material.like_count += 1
    db.session.commit()
    return jsonify({'message': '点赞成功', 'like_count': material.like_count})


@training_bp.route('/my-materials', methods=['GET'])
@jwt_required()
def get_my_materials():
    """获取我的学习资料"""
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    
    query = StudyMaterial.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    materials = query.order_by(StudyMaterial.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [m.to_dict() for m in materials.items],
        'total': materials.total,
        'pages': materials.pages,
        'current_page': page
    })


# ========== 考证信息 ==========

@training_bp.route('/certifications', methods=['GET'])
def get_certifications():
    """获取考证信息列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    
    query = CertificationInfo.query
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    
    certs = query.order_by(CertificationInfo.exam_date.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [c.to_dict() for c in certs.items],
        'total': certs.total,
        'pages': certs.pages,
        'current_page': page
    })
