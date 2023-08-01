from marshmallow import Schema, fields


class PostSchema(Schema):
    body = fields.Str()
    user_id = fields.Integer()
    timestamp = fields.Date()


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    posts = fields.Str
