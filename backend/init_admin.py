import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    
    if not admin:
        print("Creating default admin user...")
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
        print("Username: admin")
        print("Password: admin")
    else:
        print("Admin user already exists!")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print("You can reset password using the script: reset_admin_password.py")
