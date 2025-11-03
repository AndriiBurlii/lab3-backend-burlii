
from flask import request
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from .. import db
from ..models import User
from ..schemas import UserCreateSchema, UserOutSchema

blp = Blueprint("users", __name__, url_prefix="/api/users", description="Users")

@blp.route("", methods=["POST"])
@blp.arguments(UserCreateSchema)
@blp.response(201, UserOutSchema)
def create_user(payload):
    user = User(email=payload["email"])
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, message="User with this email already exists")
    return user

@blp.route("", methods=["GET"])
@blp.response(200, UserOutSchema(many=True))
def list_users():
    return User.query.order_by(User.id.asc()).all()
