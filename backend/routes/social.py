"""
社交动态路由
- 帖子/动态
- 评论
- 点赞
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, SocialPost, PostComment, PostLike

social_bp = Blueprint('social', __name__)


@social_bp.route('/feed', methods=['GET'])
def get_feed():
    """获取动态流"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    circle_id = request.args.get('circle_id', type=int)
    
    query = SocialPost.query.filter_by(status='active')
    
    if circle_id:
        query = query.filter_by(circle_id=circle_id)
    
    posts = query.order_by(SocialPost.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [p.to_dict(include_user=True) for p in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    })


@social_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """发布动态"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    post = SocialPost(
        user_id=user_id,
        content=data.get('content'),
        post_type=data.get('post_type', 'text'),
        images=data.get('images'),  # JSON字符串
        circle_id=data.get('circle_id'),
        tags=data.get('tags'),
        is_anonymous=data.get('is_anonymous', False)
    )
    db.session.add(post)
    
    # 更新用户发帖数
    user = User.query.get(user_id)
    user.post_count += 1
    
    db.session.commit()
    return jsonify({'message': '发布成功', 'post': post.to_dict()})


@social_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """获取帖子详情"""
    post = SocialPost.query.get_or_404(post_id)
    post.view_count += 1
    db.session.commit()
    return jsonify(post.to_dict(include_user=True, include_circle=True))


@social_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """删除帖子"""
    user_id = get_jwt_identity()
    post = SocialPost.query.get_or_404(post_id)
    
    if post.user_id != user_id:
        return jsonify({'error': '无权删除'}), 403
    
    post.status = 'deleted'
    db.session.commit()
    return jsonify({'message': '删除成功'})


@social_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    """点赞帖子"""
    user_id = get_jwt_identity()
    
    # 检查是否已点赞
    existing = PostLike.query.filter_by(
        user_id=user_id, target_id=post_id, target_type='post'
    ).first()
    
    if existing:
        return jsonify({'error': '已点赞'}), 400
    
    like = PostLike(user_id=user_id, target_id=post_id, target_type='post')
    post = SocialPost.query.get(post_id)
    post.like_count += 1
    
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': '点赞成功'})


@social_bp.route('/posts/<int:post_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    """取消点赞"""
    user_id = get_jwt_identity()
    
    like = PostLike.query.filter_by(
        user_id=user_id, target_id=post_id, target_type='post'
    ).first()
    
    if not like:
        return jsonify({'error': '未点赞'}), 400
    
    db.session.delete(like)
    post = SocialPost.query.get(post_id)
    post.like_count -= 1
    db.session.commit()
    return jsonify({'message': '取消点赞成功'})


@social_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    """获取评论列表"""
    comments = PostComment.query.filter_by(post_id=post_id)\
        .order_by(PostComment.created_at.desc()).all()
    return jsonify({
        'items': [c.to_dict(include_user=True) for c in comments]
    })


@social_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    """添加评论"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    comment = PostComment(
        post_id=post_id,
        user_id=user_id,
        parent_id=data.get('parent_id'),
        content=data.get('content')
    )
    db.session.add(comment)
    
    # 更新评论数
    post = SocialPost.query.get(post_id)
    post.comment_count += 1
    
    db.session.commit()
    return jsonify({'message': '评论成功', 'comment': comment.to_dict()})


# 导入 User 用于更新计数
from models import User
