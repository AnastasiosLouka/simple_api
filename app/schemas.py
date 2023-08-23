from marshmallow import Schema, fields


class PostSchema(Schema):
    body = fields.Str()
    user_id = fields.Integer()
    timestamp = fields.Date()
    id = fields.Integer


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
    email = fields.Email()
    posts = fields.Nested(PostSchema(many=True))
