"""
跳蚤市场路由
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from models import db, FleaItem, FleaWanted

flea_bp = Blueprint('flea', __name__)


# ========== 二手物品 ==========

@flea_bp.route('/items', methods=['GET'])
def get_items():
    """获取物品列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    keyword = request.args.get('keyword', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    query = FleaItem.query.filter_by(status='on_sale')
    
    if category:
        query = query.filter_by(category=category)
    if keyword:
        query = query.filter(
            or_(
                FleaItem.title.contains(keyword),
                FleaItem.description.contains(keyword)
            )
        )
    if min_price is not None:
        query = query.filter(FleaItem.price >= min_price)
    if max_price is not None:
        query = query.filter(FleaItem.price <= max_price)
    
    items = query.order_by(FleaItem.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [i.to_dict(include_seller=True) for i in items.items],
        'total': items.total,
        'pages': items.pages,
        'current_page': page
    })


@flea_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """获取物品详情"""
    item = FleaItem.query.get_or_404(item_id)
    item.view_count += 1
    db.session.commit()
    return jsonify(item.to_dict(include_seller=True))


@flea_bp.route('/items', methods=['POST'])
@jwt_required()
def publish_item():
    """发布物品"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    item = FleaItem(
        seller_id=user_id,
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        price=data.get('price'),
        original_price=data.get('original_price'),
        condition=data.get('condition'),
        images=data.get('images'),
        trade_location=data.get('trade_location'),
        trade_method=data.get('trade_method'),
        is_bargain_allowed=data.get('is_bargain_allowed', True)
    )
    db.session.add(item)
    db.session.commit()
    
    return jsonify({'message': '发布成功', 'item': item.to_dict()})


@flea_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    """更新物品信息"""
    user_id = int(get_jwt_identity())
    item = FleaItem.query.get_or_404(item_id)
    
    if item.seller_id != user_id:
        return jsonify({'error': '无权修改'}), 403
    
    data = request.get_json()
    allowed_fields = ['title', 'description', 'price', 'condition', 
                      'images', 'trade_location', 'trade_method', 'status']
    
    for field in allowed_fields:
        if field in data:
            setattr(item, field, data[field])
    
    db.session.commit()
    return jsonify({'message': '更新成功', 'item': item.to_dict()})


@flea_bp.route('/items/<int:item_id>/favorite', methods=['POST'])
@jwt_required()
def favorite_item(item_id):
    """收藏物品"""
    user_id = get_jwt_identity()
    from models import UserFavorite
    
    existing = UserFavorite.query.filter_by(
        user_id=user_id, target_id=item_id, target_type='flea_item'
    ).first()
    
    if existing:
        return jsonify({'error': '已收藏'}), 400
    
    item = FleaItem.query.get(item_id)
    favorite = UserFavorite(
        user_id=user_id,
        target_id=item_id,
        target_type='flea_item',
        title=item.title
    )
    db.session.add(favorite)
    item.favorite_count += 1
    db.session.commit()
    
    return jsonify({'message': '收藏成功'})


@flea_bp.route('/my-items', methods=['GET'])
@jwt_required()
def get_my_items():
    """获取我发布的物品"""
    user_id = get_jwt_identity()
    status = request.args.get('status', '')
    
    query = FleaItem.query.filter_by(seller_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    items = query.order_by(FleaItem.created_at.desc()).all()
    return jsonify({'items': [i.to_dict() for i in items]})


# ========== 求购信息 ==========

@flea_bp.route('/wanted', methods=['GET'])
def get_wanteds():
    """获取求购列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', '')
    
    query = FleaWanted.query.filter_by(status='active')
    
    if category:
        query = query.filter_by(category=category)
    
    wanteds = query.order_by(FleaWanted.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [w.to_dict(include_user=True) for w in wanteds.items],
        'total': wanteds.total,
        'pages': wanteds.pages,
        'current_page': page
    })


@flea_bp.route('/wanted', methods=['POST'])
@jwt_required()
def create_wanted():
    """发布求购"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    wanted = FleaWanted(
        user_id=user_id,
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        max_price=data.get('max_price')
    )
    db.session.add(wanted)
    db.session.commit()
    
    return jsonify({'message': '发布成功', 'wanted': wanted.to_dict()})


@flea_bp.route('/my-wanteds', methods=['GET'])
@jwt_required()
def get_my_wanteds():
    """获取我的求购"""
    user_id = get_jwt_identity()
    wanteds = FleaWanted.query.filter_by(user_id=user_id).all()
    return jsonify({'items': [w.to_dict() for w in wanteds]})
