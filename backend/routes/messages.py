"""
私信/聊天路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PrivateMessage
from sqlalchemy import or_

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """获取会话列表"""
    user_id = get_jwt_identity()
    
    # 获取所有相关的消息，按对话分组
    messages = PrivateMessage.query.filter(
        or_(
            PrivateMessage.sender_id == user_id,
            PrivateMessage.receiver_id == user_id
        )
    ).order_by(PrivateMessage.created_at.desc()).all()
    
    # 按对话伙伴分组
    conversations = {}
    for msg in messages:
        other_id = msg.receiver_id if msg.sender_id == user_id else msg.sender_id
        if other_id not in conversations:
            conversations[other_id] = {
                'user_id': other_id,
                'last_message': msg.to_dict(),
                'unread_count': 0
            }
        if msg.receiver_id == user_id and not msg.is_read:
            conversations[other_id]['unread_count'] += 1
    
    return jsonify({'items': list(conversations.values())})


@messages_bp.route('/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_messages(other_user_id):
    """获取与某用户的聊天记录"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    messages = PrivateMessage.query.filter(
        or_(
            (PrivateMessage.sender_id == user_id) & (PrivateMessage.receiver_id == other_user_id),
            (PrivateMessage.sender_id == other_user_id) & (PrivateMessage.receiver_id == user_id)
        )
    ).order_by(PrivateMessage.created_at.desc())\
    .paginate(page=page, per_page=per_page, error_out=False)
    
    # 标记为已读
    for msg in messages.items:
        if msg.receiver_id == user_id and not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    return jsonify({
        'items': [m.to_dict(include_sender=True) for m in reversed(messages.items)],
        'total': messages.total,
        'pages': messages.pages,
        'current_page': page
    })


@messages_bp.route('', methods=['POST'])
@jwt_required()
def send_message():
    """发送私信"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    message = PrivateMessage(
        sender_id=user_id,
        receiver_id=data.get('receiver_id'),
        content=data.get('content'),
        message_type=data.get('message_type', 'text')
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'message': '发送成功', 'data': message.to_dict()})


@messages_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """获取未读消息数"""
    user_id = get_jwt_identity()
    count = PrivateMessage.query.filter_by(
        receiver_id=user_id, is_read=False
    ).count()
    return jsonify({'unread_count': count})
