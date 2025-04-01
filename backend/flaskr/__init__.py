import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
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
    CORS(app)

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

    # register error handling for bad requests, 404 and 400
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error=str(e)), 400

    from .blueprints.api.v1 import auth
    app.register_blueprint(auth.bp)

    from .blueprints.api.v1 import movie
    app.register_blueprint(movie.bp)

    from .blueprints.api.v1 import tv
    app.register_blueprint(tv.bp)

    from .blueprints.api.v1 import search
    app.register_blueprint(search.bp)

    return app
