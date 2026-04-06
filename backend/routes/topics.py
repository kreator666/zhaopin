"""
兴趣话题模块 - 独立话题系统
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Topic, TopicReply, User
from datetime import datetime

topics_bp = Blueprint('topics', __name__, url_prefix='/api/topics')


@topics_bp.route('', methods=['GET'])
def get_topics():
    """获取话题列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    tag = request.args.get('tag', '')
    search = request.args.get('search', '')
    user_id = request.args.get('user_id', type=int)
    
    query = Topic.query.filter_by(status='open')
    
    # 按用户筛选
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    # 按标签筛选
    if tag:
        query = query.filter(Topic.tags.contains(tag))
    
    # 按关键词搜索
    if search:
        query = query.filter(
            db.or_(
                Topic.title.contains(search),
                Topic.content.contains(search)
            )
        )
    
    # 排序：置顶优先，然后按最后回复时间
    topics = query.order_by(Topic.is_pinned.desc(), Topic.last_reply_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [t.to_dict(include_user=True) for t in topics.items],
        'total': topics.total,
        'pages': topics.pages,
        'current_page': page
    })


@topics_bp.route('', methods=['POST'])
@jwt_required()
def create_topic():
    """创建话题"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    data = request.get_json()
    
    # 验证必填字段
    if not data.get('title'):
        return jsonify({'error': '话题标题不能为空'}), 400
    
    # 处理标签
    tags = data.get('tags', [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]
    
    # 处理可见范围
    visibility = data.get('visibility', 'public')
    if visibility == 'school_only' and not user.school_name:
        return jsonify({'error': '请先完善学校信息'}), 400
    
    topic = Topic(
        user_id=user_id,
        title=data['title'],
        content=data.get('content', ''),
        tags=tags,
        visibility=visibility,
        status='open'
    )
    
    db.session.add(topic)
    db.session.commit()
    
    return jsonify({
        'message': '话题发布成功',
        'topic': topic.to_dict(include_user=True)
    }), 201


@topics_bp.route('/<int:topic_id>', methods=['GET'])
@jwt_required(optional=True)
def get_topic(topic_id):
    """获取话题详情"""
    topic = Topic.query.get_or_404(topic_id)
    user_id = get_jwt_identity()
    
    # 检查可见范围
    if topic.visibility == 'school_only':
        if not user_id:
            return jsonify({'error': '请先登录'}), 401
        current_user = User.query.get(int(user_id))
        if not current_user or current_user.school_name != topic.user.school_name:
            return jsonify({'error': '该话题仅同校可见'}), 403
    
    # 增加浏览量
    topic.view_count += 1
    db.session.commit()
    
    return jsonify(topic.to_dict(include_user=True))


@topics_bp.route('/<int:topic_id>', methods=['PUT'])
@jwt_required()
def update_topic(topic_id):
    """更新话题"""
    user_id = int(get_jwt_identity())
    topic = Topic.query.get_or_404(topic_id)
    
    # 检查权限
    if topic.user_id != user_id:
        return jsonify({'error': '无权编辑此话题'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        topic.title = data['title']
    if 'content' in data:
        topic.content = data['content']
    if 'tags' in data:
        tags = data['tags']
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]
        topic.tags = tags
    if 'visibility' in data:
        topic.visibility = data['visibility']
    
    db.session.commit()
    
    return jsonify({
        'message': '更新成功',
        'topic': topic.to_dict(include_user=True)
    })


@topics_bp.route('/<int:topic_id>', methods=['DELETE'])
@jwt_required()
def delete_topic(topic_id):
    """删除话题"""
    user_id = int(get_jwt_identity())
    topic = Topic.query.get_or_404(topic_id)
    
    # 检查权限（作者可删除）
    if topic.user_id != user_id:
        return jsonify({'error': '无权删除此话题'}), 403
    
    db.session.delete(topic)
    db.session.commit()
    
    return jsonify({'message': '删除成功'})


@topics_bp.route('/<int:topic_id>/close', methods=['POST'])
@jwt_required()
def close_topic(topic_id):
    """关闭话题"""
    user_id = int(get_jwt_identity())
    topic = Topic.query.get_or_404(topic_id)
    
    if topic.user_id != user_id:
        return jsonify({'error': '无权操作'}), 403
    
    topic.status = 'closed'
    db.session.commit()
    
    return jsonify({'message': '话题已关闭'})


@topics_bp.route('/<int:topic_id>/solve', methods=['POST'])
@jwt_required()
def solve_topic(topic_id):
    """标记话题为已解决"""
    user_id = int(get_jwt_identity())
    topic = Topic.query.get_or_404(topic_id)
    
    if topic.user_id != user_id:
        return jsonify({'error': '无权操作'}), 403
    
    topic.status = 'solved'
    db.session.commit()
    
    return jsonify({'message': '话题已标记为已解决'})


# ==========================================
# 回复相关
# ==========================================

@topics_bp.route('/<int:topic_id>/replies', methods=['GET'])
def get_replies(topic_id):
    """获取话题回复列表"""
    topic = Topic.query.get_or_404(topic_id)
    
    # 只获取一级回复
    replies = TopicReply.query.filter_by(
        topic_id=topic_id,
        parent_id=None
    ).order_by(TopicReply.created_at.asc()).all()
    
    return jsonify({
        'items': [r.to_dict(include_user=True) for r in replies]
    })


@topics_bp.route('/<int:topic_id>/replies', methods=['POST'])
@jwt_required()
def create_reply(topic_id):
    """创建回复"""
    user_id = int(get_jwt_identity())
    topic = Topic.query.get_or_404(topic_id)
    
    if topic.status == 'closed':
        return jsonify({'error': '话题已关闭，无法回复'}), 400
    
    data = request.get_json()
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': '回复内容不能为空'}), 400
    
    reply = TopicReply(
        topic_id=topic_id,
        user_id=user_id,
        content=content,
        parent_id=data.get('parent_id')
    )
    
    db.session.add(reply)
    
    # 更新话题回复数和最后回复时间
    topic.reply_count += 1
    topic.last_reply_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': '回复成功',
        'reply': reply.to_dict(include_user=True)
    }), 201


@topics_bp.route('/replies/<int:reply_id>', methods=['DELETE'])
@jwt_required()
def delete_reply(reply_id):
    """删除回复"""
    user_id = int(get_jwt_identity())
    reply = TopicReply.query.get_or_404(reply_id)
    
    # 检查权限
    if reply.user_id != user_id:
        return jsonify({'error': '无权删除此回复'}), 403
    
    topic = Topic.query.get(reply.topic_id)
    
    db.session.delete(reply)
    
    # 更新话题回复数
    if topic and topic.reply_count > 0:
        topic.reply_count -= 1
    
    db.session.commit()
    
    return jsonify({'message': '删除成功'})


@topics_bp.route('/replies/<int:reply_id>/accept', methods=['POST'])
@jwt_required()
def accept_reply(reply_id):
    """采纳为最佳答案"""
    user_id = int(get_jwt_identity())
    reply = TopicReply.query.get_or_404(reply_id)
    topic = Topic.query.get(reply.topic_id)
    
    # 只有话题作者可以采纳答案
    if topic.user_id != user_id:
        return jsonify({'error': '无权操作'}), 403
    
    # 清除该话题其他回复的采纳状态
    TopicReply.query.filter_by(topic_id=reply.topic_id).update({'is_accepted': False})
    
    reply.is_accepted = True
    topic.status = 'solved'
    
    db.session.commit()
    
    return jsonify({'message': '已采纳为最佳答案'})


# ==========================================
# 标签相关
# ==========================================

@topics_bp.route('/tags', methods=['GET'])
def get_tags():
    """获取所有标签"""
    # 从所有话题中提取标签
    topics = Topic.query.all()
    tag_set = set()
    for topic in topics:
        if topic.tags:
            tag_set.update(topic.tags)
    
    return jsonify({'tags': sorted(list(tag_set))})
