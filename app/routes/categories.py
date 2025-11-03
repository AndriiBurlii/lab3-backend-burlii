
from flask import request
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from .. import db
from ..models import Category, User
from ..schemas import CategoryCreateSchema, CategoryOutSchema

blp = Blueprint("categories", __name__, url_prefix="/api/categories", description="Categories")

def _current_user_id():
    # For demo: you may pass X-User-Id header to filter results conveniently
    h = request.headers.get("X-User-Id")
    return int(h) if h is not None and h.isdigit() else None

@blp.route("", methods=["POST"])
@blp.arguments(CategoryCreateSchema)
@blp.response(201, CategoryOutSchema)
def create_category(payload):
    user_id = _current_user_id()
    is_global = payload.get("is_global", False)

    if is_global:
        owner_id = None
    else:
        # Must belong to a user if not global
        if not user_id:
            abort(400, message="Provide X-User-Id header to create user category")
        if not User.query.get(user_id):
            abort(404, message="User not found")
        owner_id = user_id

    category = Category(name=payload["name"], is_global=is_global, user_id=owner_id)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        abort(409, message="Category with this name already exists in this scope")
    return category

@blp.route("", methods=["GET"])
@blp.response(200, CategoryOutSchema(many=True))
def list_categories():
    user_id = _current_user_id()
    q = Category.query
    if user_id:
        q = q.filter(or_(Category.is_global == True, Category.user_id == user_id))  # noqa: E712
    else:
        q = q.filter(Category.is_global == True)  # noqa: E712
    return q.order_by(Category.is_global.desc(), Category.name.asc()).all()
