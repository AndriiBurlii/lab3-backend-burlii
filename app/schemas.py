from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, max=128),
    )


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserOutSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    created_at = fields.DateTime()


class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    is_global = fields.Bool(load_default=False)


class CategoryOutSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    is_global = fields.Bool()
    user_id = fields.Int(allow_none=True)


class ExpenseCreateSchema(Schema):
    # Для простоти варіанту залишаємо user_id в тілі запиту
    user_id = fields.Int(required=True)
    category_id = fields.Int(load_default=None, allow_none=True)
    amount = fields.Decimal(
        as_string=True,
        required=True,
        validate=validate.Range(min=0.01),
    )
    description = fields.Str(
        load_default=None,
        allow_none=True,
        validate=validate.Length(max=500),
    )


class ExpenseOutSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    category_id = fields.Int(allow_none=True)
    amount = fields.Decimal(as_string=True)
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime()
