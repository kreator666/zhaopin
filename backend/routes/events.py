"""
活动/约伴路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, SocialEvent, EventParticipant

events_bp = Blueprint('events', __name__)


@events_bp.route('', methods=['GET'])
def get_events():
    """获取活动列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    event_type = request.args.get('type', '')
    status = request.args.get('status', '')
    
    query = SocialEvent.query
    
    if event_type:
        query = query.filter_by(event_type=event_type)
    if status:
        query = query.filter_by(status=status)
    
    events = query.order_by(SocialEvent.start_time.asc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [e.to_dict(include_creator=True) for e in events.items],
        'total': events.total,
        'pages': events.pages,
        'current_page': page
    })


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """获取活动详情"""
    event = SocialEvent.query.get_or_404(event_id)
    return jsonify(event.to_dict(include_creator=True))


@events_bp.route('', methods=['POST'])
@jwt_required()
def create_event():
    """创建活动"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    event = SocialEvent(
        title=data.get('title'),
        description=data.get('description'),
        event_type=data.get('event_type'),
        creator_id=user_id,
        location=data.get('location'),
        location_lat=data.get('location_lat'),
        location_lng=data.get('location_lng'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        max_participants=data.get('max_participants')
    )
    db.session.add(event)
    db.session.flush()
    
    # 创建者自动参加
    participant = EventParticipant(
        event_id=event.id,
        user_id=user_id
    )
    db.session.add(participant)
    event.current_participants = 1
    
    db.session.commit()
    return jsonify({'message': '活动创建成功', 'event': event.to_dict()})


@events_bp.route('/<int:event_id>/join', methods=['POST'])
@jwt_required()
def join_event(event_id):
    """参加活动"""
    user_id = get_jwt_identity()
    event = SocialEvent.query.get_or_404(event_id)
    
    if event.status == 'full':
        return jsonify({'error': '活动已满员'}), 400
    if event.status == 'ended':
        return jsonify({'error': '活动已结束'}), 400
    
    # 检查是否已参加
    existing = EventParticipant.query.filter_by(
        event_id=event_id, user_id=user_id
    ).first()
    if existing:
        return jsonify({'error': '已参加该活动'}), 400
    
    participant = EventParticipant(event_id=event_id, user_id=user_id)
    db.session.add(participant)
    event.current_participants += 1
    
    # 检查是否满员
    if event.max_participants and event.current_participants >= event.max_participants:
        event.status = 'full'
    
    db.session.commit()
    return jsonify({'message': '参加成功'})


@events_bp.route('/<int:event_id>/leave', methods=['POST'])
@jwt_required()
def leave_event(event_id):
    """退出活动"""
    user_id = get_jwt_identity()
    
    participant = EventParticipant.query.filter_by(
        event_id=event_id, user_id=user_id
    ).first()
    
    if not participant:
        return jsonify({'error': '未参加该活动'}), 400
    
    db.session.delete(participant)
    event = SocialEvent.query.get(event_id)
    event.current_participants -= 1
    if event.status == 'full':
        event.status = 'open'
    
    db.session.commit()
    return jsonify({'message': '退出成功'})


@events_bp.route('/<int:event_id>/participants', methods=['GET'])
def get_participants(event_id):
    """获取参与者列表"""
    participants = EventParticipant.query.filter_by(event_id=event_id).all()
    return jsonify({
        'items': [p.user.to_dict() for p in participants]
    })


@events_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_events():
    """获取我的活动"""
    user_id = get_jwt_identity()
    participations = EventParticipant.query.filter_by(user_id=user_id).all()
    
    events = [p.event.to_dict() for p in participations]
    return jsonify({'items': events})
