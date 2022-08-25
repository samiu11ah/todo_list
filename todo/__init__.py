from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_marshmallow import Marshmallow

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


ma = Marshmallow()

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #     SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False
    # )

    app.config['SECRET_KEY'] = 'a3410e5f349e760123db6e01649311f9dc6866a3cb320081bc08bb0ed48f22c'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    login_manager = LoginManager()

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Bitte melden Sie sich an, um auf diese Seite zuzugreifen.'
    login_manager.init_app(app)

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_bluprint
    app.register_blueprint(auth_bluprint)

    from .main import main as main_bluprint
    app.register_blueprint(main_bluprint)
    
    from .api import api as api_bluprint
    app.register_blueprint(api_bluprint)

    return app

