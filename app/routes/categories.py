from flask import request
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from .. import db
from ..models import Category, User
from ..schemas import CategoryCreateSchema, CategoryOutSchema

blp = Blueprint(
    "categories",
    __name__,
    url_prefix="/api/categories",
    description="Categories",
)


def _current_user_id():
    """Helper to read user id from header (backward compatible with Lab 3).

    У варіанті з JWT ми все одно залишаємо X-User-Id, щоб не ламати існуючі приклади.
    """
    h = request.headers.get("X-User-Id")
    return int(h) if h is not None and h.isdigit() else None


@blp.route("", methods=["POST"])
@jwt_required()
@blp.arguments(CategoryCreateSchema)
@blp.response(201, CategoryOutSchema)
def create_category(payload):
    """Create global or user-specific category.

    - якщо is_global = true → user_id = None;
    - якщо is_global = false → очікуємо X-User-Id, шукаємо користувача.
    """
    is_global = bool(payload.get("is_global", False))
    user_id = _current_user_id() if not is_global else None

    user = None
    if not is_global:
        if not user_id:
            abort(400, message="Non-global category requires X-User-Id header")
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found")

    category = Category(
        name=payload["name"],
        is_global=is_global,
        user_id=user.id if user else None,
    )
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, message="Category with this name already exists in this scope")
    return category


@blp.route("", methods=["GET"])
@jwt_required()
@blp.response(200, CategoryOutSchema(many=True))
def list_categories():
    user_id = _current_user_id()
    q = Category.query
    if user_id:
        q = q.filter(
            or_(
                Category.is_global.is_(True),
                Category.user_id == user_id,
            )
        )
    else:
        q = q.filter(Category.is_global.is_(True))
    return q.order_by(Category.is_global.desc(), Category.name.asc()).all()
