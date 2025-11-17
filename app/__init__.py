import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import ValidationError
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    # Load base config
    app.config.from_object("config.Config")

    # JWT secret key (read from env, with safe fallback for local dev)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    # Register blueprints
    from .routes.users import blp as users_blp
    from .routes.categories import blp as categories_blp
    from .routes.expenses import blp as expenses_blp

    api.register_blueprint(users_blp)
    api.register_blueprint(categories_blp)
    api.register_blueprint(expenses_blp)

    # Init JWT after app is created
    jwt.init_app(app)

    # Simple healthcheck for convenience
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    # Marshmallow / flask-smorest validation errors
    @app.errorhandler(ValidationError)
    def handle_validation(err):
        return (
            jsonify({"message": "Validation error", "errors": err.messages}),
            400,
        )

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"message": "Not found"}), 404

    @app.errorhandler(409)
    def handle_409(err):
        return jsonify({"message": "Conflict"}), 409

    @app.errorhandler(400)
    def handle_400(err):
        return jsonify({"message": "Bad request"}), 400

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    return app
