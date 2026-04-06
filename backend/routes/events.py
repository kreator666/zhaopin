"""
活动/约伴路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, SocialEvent, EventParticipant, EventComment, EventCheckIn, EventReview, User
from datetime import datetime, timedelta

events_bp = Blueprint('events', __name__)


@events_bp.route('', methods=['GET'])
def get_events():
    """获取活动列表 - 支持高级筛选"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    event_type = request.args.get('type', '')
    status = request.args.get('status', '')
    keyword = request.args.get('keyword', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    location = request.args.get('location', '')
    
    query = SocialEvent.query
    
    # 按类型筛选
    if event_type:
        query = query.filter_by(event_type=event_type)
    
    # 按状态筛选
    if status:
        query = query.filter_by(status=status)
    
    # 按关键词搜索标题
    if keyword:
        query = query.filter(SocialEvent.title.contains(keyword))
    
    # 按地点搜索
    if location:
        query = query.filter(SocialEvent.location.contains(location))
    
    # 按时间范围筛选
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(SocialEvent.start_time >= start)
        except:
            pass
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(SocialEvent.start_time <= end)
        except:
            pass
    
    # 默认只显示招募中的活动
    if not status:
        query = query.filter(SocialEvent.status.in_(['open', 'full']))
    
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
    
    # 增加浏览量
    event.view_count = (event.view_count or 0) + 1
    db.session.commit()
    
    return jsonify(event.to_dict(include_creator=True))


@events_bp.route('', methods=['POST'])
@jwt_required()
def create_event():
    """创建活动"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # 验证必填字段
    if not data.get('title'):
        return jsonify({'error': '活动标题不能为空'}), 400
    if not data.get('start_time'):
        return jsonify({'error': '开始时间不能为空'}), 400
    if not data.get('location'):
        return jsonify({'error': '活动地点不能为空'}), 400
    
    try:
        start_time = datetime.fromisoformat(data.get('start_time'))
        end_time = None
        if data.get('end_time'):
            end_time = datetime.fromisoformat(data.get('end_time'))
    except:
        return jsonify({'error': '时间格式错误'}), 400
    
    # 验证开始时间不能早于现在
    if start_time < datetime.utcnow():
        return jsonify({'error': '开始时间不能早于当前时间'}), 400
    
    event = SocialEvent(
        title=data.get('title'),
        description=data.get('description', ''),
        event_type=data.get('event_type', 'other'),
        creator_id=user_id,
        location=data.get('location'),
        location_lat=data.get('location_lat'),
        location_lng=data.get('location_lng'),
        start_time=start_time,
        end_time=end_time,
        max_participants=data.get('max_participants'),
        cover_image=data.get('cover_image'),
        fee_type=data.get('fee_type', 'free'),
        fee_amount=data.get('fee_amount', 0),
        status='open'
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
    return jsonify({'message': '活动创建成功', 'event': event.to_dict(include_creator=True)})


@events_bp.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    """更新活动"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    # 检查权限
    if event.creator_id != int(user_id):
        return jsonify({'error': '无权编辑此活动'}), 403
    
    data = request.get_json()
    
    # 更新字段
    if 'title' in data:
        event.title = data['title']
    if 'description' in data:
        event.description = data['description']
    if 'event_type' in data:
        event.event_type = data['event_type']
    if 'location' in data:
        event.location = data['location']
    if 'location_lat' in data:
        event.location_lat = data['location_lat']
    if 'location_lng' in data:
        event.location_lng = data['location_lng']
    if 'start_time' in data:
        try:
            event.start_time = datetime.fromisoformat(data['start_time'])
        except:
            pass
    if 'end_time' in data:
        try:
            event.end_time = datetime.fromisoformat(data['end_time'])
        except:
            pass
    if 'max_participants' in data:
        event.max_participants = data['max_participants']
    if 'cover_image' in data:
        event.cover_image = data['cover_image']
    if 'fee_type' in data:
        event.fee_type = data['fee_type']
    if 'fee_amount' in data:
        event.fee_amount = data['fee_amount']
    if 'status' in data:
        event.status = data['status']
    
    db.session.commit()
    return jsonify({'message': '更新成功', 'event': event.to_dict(include_creator=True)})


@events_bp.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    """删除活动"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    if event.creator_id != int(user_id):
        return jsonify({'error': '无权删除此活动'}), 403
    
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': '删除成功'})


@events_bp.route('/<int:event_id>/join', methods=['POST'])
@jwt_required()
def join_event(event_id):
    """参加活动"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    # 检查状态
    if event.status == 'full':
        return jsonify({'error': '活动已满员'}), 400
    if event.status == 'ended':
        return jsonify({'error': '活动已结束'}), 400
    if event.status == 'cancelled':
        return jsonify({'error': '活动已取消'}), 400
    
    # 不能参加自己创建的活动（已自动参加）
    if event.creator_id == user_id:
        return jsonify({'error': '您是活动创建者，已自动参加'}), 400
    
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
    user_id = int(get_jwt_identity())
    
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
        'items': [p.user.to_dict() for p in participants],
        'total': len(participants)
    })


@events_bp.route('/<int:event_id>/comments', methods=['GET'])
def get_comments(event_id):
    """获取活动评论列表"""
    event = SocialEvent.query.get_or_404(event_id)
    
    # 只获取一级评论
    comments = EventComment.query.filter_by(
        event_id=event_id,
        parent_id=None
    ).order_by(EventComment.created_at.desc()).all()
    
    return jsonify({
        'items': [c.to_dict(include_user=True) for c in comments]
    })


@events_bp.route('/<int:event_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(event_id):
    """发表评论"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    data = request.get_json()
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
    
    comment = EventComment(
        event_id=event_id,
        user_id=user_id,
        content=content,
        parent_id=data.get('parent_id')
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'message': '评论成功',
        'comment': comment.to_dict(include_user=True)
    }), 201


@events_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """删除评论"""
    user_id = int(get_jwt_identity())
    comment = EventComment.query.get_or_404(comment_id)
    
    # 检查权限（评论作者或活动创建者）
    event = SocialEvent.query.get(comment.event_id)
    if comment.user_id != user_id and event.creator_id != user_id:
        return jsonify({'error': '无权删除此评论'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': '删除成功'})


@events_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_events():
    """获取我的活动"""
    user_id = int(get_jwt_identity())
    event_type = request.args.get('type', 'joined')  # joined, created, history
    
    if event_type == 'created':
        # 我创建的
        events = SocialEvent.query.filter_by(creator_id=user_id).all()
    elif event_type == 'history':
        # 历史活动（已结束）
        participations = EventParticipant.query.filter_by(user_id=user_id).all()
        event_ids = [p.event_id for p in participations]
        events = SocialEvent.query.filter(
            SocialEvent.id.in_(event_ids),
            SocialEvent.status.in_(['ended', 'cancelled'])
        ).all()
    else:
        # 我参加的（默认）
        participations = EventParticipant.query.filter_by(user_id=user_id).all()
        event_ids = [p.event_id for p in participations]
        events = SocialEvent.query.filter(
            SocialEvent.id.in_(event_ids),
            SocialEvent.status.notin_(['ended', 'cancelled'])
        ).all()
    
    return jsonify({'items': [e.to_dict() for e in events]})


@events_bp.route('/types', methods=['GET'])
def get_event_types():
    """获取活动类型列表"""
    types = [
        {'value': 'sports', 'label': '运动健身', 'icon': 'Basketball'},
        {'value': 'study', 'label': '学习交流', 'icon': 'Reading'},
        {'value': 'dining', 'label': '聚餐美食', 'icon': 'Food'},
        {'value': 'travel', 'label': '旅行户外', 'icon': 'MapLocation'},
        {'value': 'game', 'label': '游戏娱乐', 'icon': 'VideoPlay'},
        {'value': 'party', 'label': '社交聚会', 'icon': 'UserFilled'},
        {'value': 'other', 'label': '其他', 'icon': 'More'}
    ]
    return jsonify({'items': types})


@events_bp.route('/check-status', methods=['POST'])
def check_and_update_status():
    """检查并更新活动状态（定时任务调用）"""
    now = datetime.utcnow()
    
    # 更新进行中的活动
    SocialEvent.query.filter(
        SocialEvent.start_time <= now,
        SocialEvent.end_time > now,
        SocialEvent.status.notin_(['ongoing', 'ended', 'cancelled'])
    ).update({'status': 'ongoing'})
    
    # 更新已结束的活动
    SocialEvent.query.filter(
        SocialEvent.end_time <= now,
        SocialEvent.status.notin_(['ended', 'cancelled'])
    ).update({'status': 'ended'})
    
    db.session.commit()
    
    return jsonify({'message': '状态更新完成'})


# ==========================================
# 签到相关
# ==========================================

@events_bp.route('/<int:event_id>/checkin', methods=['POST'])
@jwt_required()
def check_in(event_id):
    """活动签到"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    # 检查是否已报名
    participant = EventParticipant.query.filter_by(
        event_id=event_id, user_id=user_id
    ).first()
    if not participant:
        return jsonify({'error': '请先报名活动'}), 400
    
    # 检查活动状态
    if event.status not in ['ongoing', 'ended']:
        return jsonify({'error': '活动尚未开始'}), 400
    
    # 检查是否已签到
    existing = EventCheckIn.query.filter_by(
        event_id=event_id, user_id=user_id
    ).first()
    if existing:
        return jsonify({'error': '已签到'}), 400
    
    data = request.get_json()
    check_in = EventCheckIn(
        event_id=event_id,
        user_id=user_id,
        check_in_method=data.get('method', 'manual')
    )
    db.session.add(check_in)
    db.session.commit()
    
    return jsonify({
        'message': '签到成功',
        'checkin': check_in.to_dict()
    })


@events_bp.route('/<int:event_id>/checkin/status', methods=['GET'])
@jwt_required()
def get_checkin_status(event_id):
    """获取签到状态"""
    user_id = int(get_jwt_identity())
    check_in = EventCheckIn.query.filter_by(
        event_id=event_id, user_id=user_id
    ).first()
    
    return jsonify({
        'checked_in': check_in is not None,
        'check_in_time': check_in.checked_in_at.isoformat() if check_in else None
    })


@events_bp.route('/<int:event_id>/checkins', methods=['GET'])
@jwt_required()
def get_checkin_list(event_id):
    """获取签到列表（仅创建者）"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    if event.creator_id != user_id:
        return jsonify({'error': '无权查看'}), 403
    
    checkins = EventCheckIn.query.filter_by(event_id=event_id).all()
    return jsonify({
        'items': [c.to_dict(include_user=True) for c in checkins],
        'total': len(checkins)
    })


# ==========================================
# 评价相关
# ==========================================

@events_bp.route('/<int:event_id>/reviews', methods=['GET'])
def get_reviews(event_id):
    """获取活动评价列表"""
    reviews = EventReview.query.filter_by(event_id=event_id).all()
    return jsonify({
        'items': [r.to_dict(include_users=True) for r in reviews],
        'total': len(reviews)
    })


@events_bp.route('/<int:event_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(event_id):
    """发表评价"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    # 检查活动是否已结束
    if event.status != 'ended':
        return jsonify({'error': '活动未结束，暂不能评价'}), 400
    
    # 检查是否已签到
    check_in = EventCheckIn.query.filter_by(
        event_id=event_id, user_id=user_id
    ).first()
    if not check_in:
        return jsonify({'error': '未签到，无法评价'}), 400
    
    data = request.get_json()
    reviewee_id = data.get('reviewee_id')
    rating = data.get('rating')
    content = data.get('content', '')
    
    if not reviewee_id:
        return jsonify({'error': '请选择评价对象'}), 400
    if not rating or not (1 <= rating <= 5):
        return jsonify({'error': '请给出1-5星评价'}), 400
    
    # 检查是否已评价
    existing = EventReview.query.filter_by(
        event_id=event_id,
        reviewer_id=user_id,
        reviewee_id=reviewee_id
    ).first()
    if existing:
        return jsonify({'error': '已评价过该用户'}), 400
    
    review = EventReview(
        event_id=event_id,
        reviewer_id=user_id,
        reviewee_id=reviewee_id,
        rating=rating,
        content=content
    )
    db.session.add(review)
    db.session.commit()
    
    return jsonify({
        'message': '评价成功',
        'review': review.to_dict(include_users=True)
    }), 201


@events_bp.route('/<int:event_id>/reviews/pending', methods=['GET'])
@jwt_required()
def get_pending_reviews(event_id):
    """获取待评价列表"""
    user_id = int(get_jwt_identity())
    event = SocialEvent.query.get_or_404(event_id)
    
    # 获取已签到但未评价的参与者
    checkins = EventCheckIn.query.filter_by(event_id=event_id).all()
    reviewed_ids = {r.reviewee_id for r in EventReview.query.filter_by(
        event_id=event_id, reviewer_id=user_id
    ).all()}
    
    pending = []
    for checkin in checkins:
        if checkin.user_id != user_id and checkin.user_id not in reviewed_ids:
            pending.append(checkin.user.to_dict())
    
    return jsonify({'items': pending})
