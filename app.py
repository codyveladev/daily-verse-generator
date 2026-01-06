# app.py
from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models.users import db, User
from routes import auth_bp, user_bp, community_bp
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.py (inside create_app function)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(community_bp, url_prefix="/community")

    # Create tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)