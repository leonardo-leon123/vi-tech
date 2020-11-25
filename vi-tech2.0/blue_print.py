from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import configure_uploads, IMAGES, UploadSet


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config['SECRET_KEY'] = 'VI-TECH'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'

    images = UploadSet('images',IMAGES)
    configure_uploads(app,images)   

    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = "No tienes Acceso a esta página. Por Favor inicia sesión o crea una cuenta"

    from database import User


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app import app as app_blueprint
    app.register_blueprint(app_blueprint)

    return app
