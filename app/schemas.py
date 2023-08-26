from marshmallow import Schema, fields


class CommentSchema(Schema):
    id = fields.Integer()
    body = fields.Str()
    timestamp = fields.Date()
    user_id = fields.Integer()
    post_id = fields.Integer()


class PostSchema(Schema):
    body = fields.Str()
    user_id = fields.Integer()
    timestamp = fields.Date()
    id = fields.Integer()
    comments = fields.Nested(CommentSchema(many=True))


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
    email = fields.Email()
    posts = fields.Nested(PostSchema(many=True))
