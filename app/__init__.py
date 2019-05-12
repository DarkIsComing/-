from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap
db=SQLAlchemy()
bootstrap=Bootstrap()

def create_app():
    app=Flask(__name__)
    app.config.from_object('Config')

    db.init_app(app)
    bootstrap.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #from .main import main as m
    return app