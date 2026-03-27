from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册路由
    from routes.auth import auth_bp
    from routes.jobs import jobs_bp
    from routes.resumes import resumes_bp
    from routes.applications import applications_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(resumes_bp, url_prefix='/api/resume')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    
    # 创建数据库表
    with app.app_context():
        import os
        # 获取实例目录的绝对路径
        instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        os.makedirs(instance_path, exist_ok=True)
        db.create_all()
        print("数据库表已创建！")
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': '服务器运行正常'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
