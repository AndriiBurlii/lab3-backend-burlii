
from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    categories = db.relationship("Category", backref="owner", lazy=True)
    expenses = db.relationship("Expense", backref="user", lazy=True)

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    is_global = db.Column(db.Boolean, default=False, nullable=False)
    # If not global, belongs to a user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Uniqueness: global names unique among global; per-user unique among that user's categories
    __table_args__ = (
        db.UniqueConstraint("name", "is_global", name="uq_category_name_global"),
        db.UniqueConstraint("name", "user_id", name="uq_category_name_user"),
    )

    expenses = db.relationship("Expense", backref="category", lazy=True)

class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
