from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        r"/static/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "OPTIONS"]
        }
    })
    
    # 注册路由
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.jobs import jobs_bp
    from routes.resumes import resumes_bp
    from routes.applications import applications_bp
    from routes.interview import interview_bp
    from routes.training import training_bp
    from routes.social import social_bp
    from routes.circles import circles_bp
    from routes.events import events_bp
    from routes.messages import messages_bp
    from routes.flea import flea_bp
    from routes.upload import upload_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(resumes_bp, url_prefix='/api/resume')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(interview_bp, url_prefix='/api/interview')
    app.register_blueprint(training_bp, url_prefix='/api/training')
    app.register_blueprint(social_bp, url_prefix='/api/social')
    app.register_blueprint(circles_bp, url_prefix='/api/circles')
    app.register_blueprint(events_bp, url_prefix='/api/events')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(flea_bp, url_prefix='/api/flea')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    
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
