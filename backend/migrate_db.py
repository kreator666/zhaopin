"""
数据库迁移脚本
为 training_courses 表添加缺失的字段
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'jobs.db')


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database not found: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='training_courses'")
        if not cursor.fetchone():
            print("Table 'training_courses' does not exist")
            conn.close()
            return
        
        # Get existing columns
        cursor.execute("PRAGMA table_info(training_courses)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Existing columns: {columns}")
        
        # Add created_by column if not exists
        if 'created_by' not in columns:
            print("Adding 'created_by' column...")
            cursor.execute("ALTER TABLE training_courses ADD COLUMN created_by INTEGER")
            print("  'created_by' column added")
        
        # Add updated_at column if not exists
        if 'updated_at' not in columns:
            print("Adding 'updated_at' column...")
            cursor.execute("ALTER TABLE training_courses ADD COLUMN updated_at DATETIME")
            print("  'updated_at' column added")
        
        conn.commit()
        print("\nMigration completed!")
        
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()
