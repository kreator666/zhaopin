"""
培训学习模块路由
- 课程
- 学习资料
- 考证信息
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, TrainingCourse, CourseEnrollment, StudyMaterial, CertificationInfo

training_bp = Blueprint('training', __name__)


# ========== 课程 ==========

@training_bp.route('/courses', methods=['GET'])
def get_courses():
    """获取课程列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    level = request.args.get('level', '')
    is_online = request.args.get('is_online', '')
    
    query = TrainingCourse.query.filter_by(status='active')
    
    if category:
        query = query.filter_by(category=category)
    if level:
        query = query.filter_by(level=level)
    if is_online:
        query = query.filter_by(is_online=is_online.lower() == 'true')
    
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
    """获取课程详情"""
    course = TrainingCourse.query.get_or_404(course_id)
    return jsonify(course.to_dict(include_stats=True))


@training_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@jwt_required()
def enroll_course(course_id):
    """报名课程"""
    user_id = get_jwt_identity()
    course = TrainingCourse.query.get_or_404(course_id)
    
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


@training_bp.route('/my-courses', methods=['GET'])
@jwt_required()
def get_my_courses():
    """获取我的课程"""
    user_id = get_jwt_identity()
    status = request.args.get('status', '')
    
    query = CourseEnrollment.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    enrollments = query.all()
    return jsonify({
        'items': [e.to_dict(include_course=True) for e in enrollments]
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
    user_id = get_jwt_identity()
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


@training_bp.route('/materials/<int:material_id>/download', methods=['POST'])
def download_material(material_id):
    """下载资料（计数）"""
    material = StudyMaterial.query.get_or_404(material_id)
    material.download_count += 1
    db.session.commit()
    return jsonify({'download_url': material.file_url})


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
