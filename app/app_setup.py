from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_filename='config_base'):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    # app.config.from_pyfile(config_filename)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
