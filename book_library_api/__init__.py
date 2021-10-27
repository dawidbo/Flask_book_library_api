from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# app = Flask(__name__)
# app.config.from_object(Config)


# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# results = db.session.execute("select 1 union all select 2")
# for row in results:
#     print(row)

# application factory prod dev test

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from book_library_api.commands import db_manage_bp
    from book_library_api.errors import errors_bp
    from book_library_api.authors import authors_bp
    from book_library_api.books import books_bp
    from book_library_api.auth import auth_bp
    app.register_blueprint(db_manage_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(authors_bp, url_prefix='/api/v1')
    app.register_blueprint(books_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    return app

# from book_library_api import authors
# from book_library_api import models
# from book_library_api.commands import db_manage_commands
# from book_library_api import errors


