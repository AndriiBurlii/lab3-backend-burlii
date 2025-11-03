
from flask import Flask, jsonify
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # Load config from file if present
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    from .models import User, Category, Expense  # noqa: F401
    from .routes.users import blp as users_blp
    from .routes.categories import blp as categories_blp
    from .routes.expenses import blp as expenses_blp

    api.register_blueprint(users_blp)
    api.register_blueprint(categories_blp)
    api.register_blueprint(expenses_blp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    # Global error handlers
    from marshmallow import ValidationError
    @app.errorhandler(ValidationError)
    def handle_marshmallow_error(err):
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"message": "Not found"}), 404

    @app.errorhandler(409)
    def handle_409(err):
        return jsonify({"message": "Conflict"}), 409

    @app.errorhandler(400)
    def handle_400(err):
        return jsonify({"message": "Bad request"}), 400

    return app
