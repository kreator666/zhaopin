"""
清理数据库所有数据，保留表结构
"""
from app import create_app
from models import db

app = create_app()

with app.app_context():
    # 获取所有表名
    from sqlalchemy import text
    
    # 禁用外键约束
    db.session.execute(text('PRAGMA foreign_keys = OFF'))
    
    # 获取所有表
    result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'alembic_%'"))
    tables = [row[0] for row in result]
    
    print(f'Found {len(tables)} tables: {tables}')
    
    # 清空每个表
    for table in tables:
        try:
            db.session.execute(text(f'DELETE FROM {table}'))
            print(f'[OK] Cleared table: {table}')
        except Exception as e:
            print(f'[ERR] Failed to clear {table}: {e}')
    
    # 重置自增ID
    for table in tables:
        try:
            db.session.execute(text(f"DELETE FROM sqlite_sequence WHERE name='{table}'"))
        except:
            pass
    
    # 重新启用外键约束
    db.session.execute(text('PRAGMA foreign_keys = ON'))
    
    db.session.commit()
    print('\n[OK] All data cleared!')
