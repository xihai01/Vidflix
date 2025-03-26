import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

def create_app(test_config=None):
    load_dotenv()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    )

    JWTManager(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database import db
    db.init_db()

    from .database import seed
    seed.init_seed(app)

    from .blueprints import auth
    app.register_blueprint(auth.bp)

    from .blueprints import movie
    app.register_blueprint(movie.bp)

    from .blueprints import tv
    app.register_blueprint(tv.bp)

    return app
