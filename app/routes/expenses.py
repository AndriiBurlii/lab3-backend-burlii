from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .. import db
from ..models import Expense, User, Category
from ..schemas import ExpenseCreateSchema, ExpenseOutSchema

blp = Blueprint(
    "expenses",
    __name__,
    url_prefix="/api/expenses",
    description="Expenses",
)


@blp.route("", methods=["POST"])
@jwt_required()
@blp.arguments(ExpenseCreateSchema)
@blp.response(201, ExpenseOutSchema)
def create_expense(payload):
    user_id = payload["user_id"]
    user = User.query.get(user_id)
    if not user:
        abort(404, message="User not found")

    category_id = payload.get("category_id")
    category = None
    if category_id is not None:
        category = Category.query.get(category_id)
        if not category:
            abort(404, message="Category not found")

    expense = Expense(
        user_id=user_id,
        category_id=category_id,
        amount=payload["amount"],
        description=payload.get("description"),
    )
    db.session.add(expense)
    db.session.commit()
    return expense


@blp.route("", methods=["GET"])
@jwt_required()
@blp.response(200, ExpenseOutSchema(many=True))
def list_expenses():
    # For demo simplicity, list all
    return Expense.query.order_by(Expense.created_at.desc()).all()
