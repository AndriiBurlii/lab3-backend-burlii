from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required

from .. import db
from ..models import User
from ..schemas import UserCreateSchema, UserOutSchema, UserLoginSchema

blp = Blueprint(
    "users",
    __name__,
    url_prefix="/api/users",
    description="Users & authentication",
)


@blp.route("", methods=["POST"])
@blp.arguments(UserCreateSchema)
@blp.response(201, UserOutSchema)
def register_user(payload):
    """
    Реєстрація користувача (Lab 4).

    Приймає email + password, хешує пароль через passlib.pbkdf2_sha256
    та зберігає у базі. При дублюванні email повертає 409.
    """
    user = User(
        email=payload["email"],
        password=pbkdf2_sha256.hash(payload["password"]),
    )
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, message="User with this email already exists")
    return user


@blp.route("/login", methods=["POST"])
@blp.arguments(UserLoginSchema)
def login(payload):
    """
    Логін користувача.

    Якщо email/пароль некоректні або хеш у старому форматі –
    повертаємо 401, а не 500 Internal Server Error.
    """
    user = User.query.filter_by(email=payload["email"]).first()

    # Якщо користувача з таким email немає
    if not user:
        abort(401, message="Invalid email or password")

    try:
        # Перевіряємо пароль проти збереженого хеша
        if not pbkdf2_sha256.verify(payload["password"], user.password):
            abort(401, message="Invalid email or password")
    except Exception:
        # Будь-яка помилка при валідації хеша = невалідний пароль/хеш
        abort(401, message="Invalid email or password")

    # Якщо все ок - видаємо JWT
    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}, 200


@blp.route("", methods=["GET"])
@jwt_required()
@blp.response(200, UserOutSchema(many=True))
def list_users():
    """
    Повертає список усіх користувачів.
    Доступ лише з валідним JWT-токеном.
    """
    return User.query.order_by(User.id.asc()).all()
