"""
文件上传路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
from datetime import datetime

upload_bp = Blueprint('upload', __name__)

# 允许的文件类型
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_FILE_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'rar'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_filename(original_filename):
    """生成安全的文件名"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    ext = original_filename.rsplit('.', 1)[1].lower()
    return f"{timestamp}_{secure_filename(original_filename)}"


@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': '不支持的文件类型'}), 400
    
    # 创建上传目录
    upload_folder = os.path.join('static', 'uploads', 'images')
    os.makedirs(upload_folder, exist_ok=True)
    
    # 保存文件
    filename = generate_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    # 返回URL
    file_url = f'/static/uploads/images/{filename}'
    return jsonify({
        'message': '上传成功',
        'url': file_url,
        'filename': filename
    })


@upload_bp.route('/file', methods=['POST'])
@jwt_required()
def upload_file():
    """上传文件（学习资料等）"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    if not allowed_file(file.filename, ALLOWED_FILE_EXTENSIONS | ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': '不支持的文件类型'}), 400
    
    # 检查文件大小
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_CONTENT_LENGTH:
        return jsonify({'error': '文件超过最大限制16MB'}), 400
    
    # 创建上传目录
    upload_folder = os.path.join('static', 'uploads', 'files')
    os.makedirs(upload_folder, exist_ok=True)
    
    # 保存文件
    filename = generate_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    file_url = f'/static/uploads/files/{filename}'
    return jsonify({
        'message': '上传成功',
        'url': file_url,
        'filename': filename,
        'size': file_size
    })


@upload_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传头像"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return jsonify({'error': '只支持图片文件'}), 400
    
    upload_folder = os.path.join('static', 'uploads', 'avatars')
    os.makedirs(upload_folder, exist_ok=True)
    
    filename = generate_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    file_url = f'/static/uploads/avatars/{filename}'
    return jsonify({
        'message': '头像上传成功',
        'url': file_url
    })
