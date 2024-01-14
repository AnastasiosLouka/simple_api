from app import app, db
from flask import jsonify, request
from app.models import User, Post, Comment
from flask_jwt_extended import create_access_token, jwt_required


# Create, Update, Get, Delete one post from db
@app.route("/post/<post_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_post(post_id):
    if request.method == "DELETE":
        post = Post.get_by_id(post_id)
        if post is None:
            return jsonify({"title": "There is no post", "msg": "No post deleted"}), 400
        post.delete()
        return jsonify({"title": "Post deleted", "msg": "Post deleted from db"}), 204

    elif request.method == "PUT":
        try:
            data = request.get_json(force=True)
        except Exception as error:
            return jsonify({"title": "request failed", "msg": str(error)}), 400
        body = data.get("body")
        if body is None:
            return (
                jsonify({"title": "There is no body", "msg": "body is required"}),
                400,
            )
        post = Post.get_by_id(post_id)
        if post is None:
            return (
                jsonify(
                    {"title": "There is no post", "msg": "Post could not updated to db"}
                ),
                400,
            )
        post.body = body
        try:
            post.save()
            return jsonify({"title": "Post updated", "msg": "Post updated to db"}), 200
        except Exception as error:
            db.session.rollback()
            return jsonify({"title": "save failed", "msg": str(error)}), 400

    else:
        post = Post.get_by_id(post_id)
        if post is None:
            return jsonify({"title": "There is no post", "msg": "No post found"}), 400
        return jsonify(Post.__schema__().dump(post)), 200


@app.route("/post", methods=["POST"])
@jwt_required()
def add_post():
    try:
        data = request.get_json(force=True)
    except Exception as error:
        return jsonify({"title": "request failed", "msg": str(error)}), 400
    body = data.get("body")
    user_id = data.get("user_id")
    if not body or not user_id:
        return (
            jsonify({"title": "Post failed", "msg": "body and user_id are required"}),
            400,
        )
    post = Post(body=body, user_id=user_id)
    try:
        post.save()
        return jsonify({"title": "Post saved", "msg": "Post saved to database"}), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"title": "save failed", "msg": str(error)}), 400


# Get all posts from db
@app.route("/posts", methods=["GET"])
@jwt_required()
def manage_posts():
    posts = Post.get_all()
    return jsonify(Post.__schema__(many=True).dump(posts)), 200


# Create, Update, Get, Delete one user from db
@app.route("/user", methods=["POST"])
# @jwt_required()
def add_user():
    try:
        data = request.get_json(force=True)
    except Exception as error:
        return jsonify({"title": "request failed", "msg": str(error)}), 400
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return (
            jsonify(
                {"title": "Save failed", "msg": "username and password are required"}
            ),
            400,
        )
    user = User(username=username)
    user.set_password(password)
    try:
        user.save()
        return jsonify({"title": "User saved", "msg": "User saved to db"}), 201
    except Exception as error:
        db.session.rollback()
        return jsonify({"title": "save failed", "msg": str(error)}), 400


@app.route("/user/<user_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_user(user_id):
    if request.method == "PUT":
        try:
            data = request.get_json(force=True)
        except Exception as error:
            return jsonify({"title": "request failed", "msg": str(error)}), 400
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return (
                jsonify(
                    {
                        "title": "Save failed",
                        "msg": "username and password are required",
                    }
                ),
                400,
            )
        user = User.get_by_id(user_id)
        if not user:
            return jsonify({"title": "Save failed", "msg": "There is no user"}), 400
        user.username = username
        user.set_password(password)
        try:
            user.save()
            return jsonify({"title": "User updated", "msg": "User updated to db"}), 200
        except Exception as error:
            db.session.rollback()
            return jsonify({"title": "save failed", "msg": str(error)}), 400

    elif request.method == "DELETE":
        user = User.get_by_id(user_id)
        if user is None:
            return jsonify({"msg": "no user deleted"}), 400
        user.delete()
        return jsonify({"title": "User deleted", "msg": "User deleted from db"}), 204

    else:  # request.method == "GET"
        user = User.get_by_id(user_id)

        if user is None:
            return jsonify({"title": "There in no user", "msg": "user not found"}), 400

        return jsonify(User.__schema__().dump(user)), 200


# Get all user from db
@app.route("/users", methods=["GET"])
@jwt_required()
def manage_users():
    users = User.get_all()
    return jsonify(User.__schema__(many=True).dump(users)), 200


# Create,Update,Get,Delete a comment from db
@app.route("/comment/<comment_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def manage_comment(comment_id):
    if request.method == "DELETE":
        comment = Comment.get_by_id(comment_id)
        if comment is None:
            return (
                jsonify({"title": "There is no comment", "msg": "No comment deleted"}),
                400,
            )
        comment.delete()
        return (
            jsonify({"title": "Comment deleted", "msg": "Comment deleted from db"}),
            204,
        )
    elif request.method == "PUT":
        try:
            data = request.get_json(force=True)
        except Exception as error:
            return jsonify({"title": "request failed", "msg": str(error)}), 400
        body = data.get("body")
        if body is None:
            return (
                jsonify({"title": "There is no body", "msg": "body is required"}),
                400,
            )
        comment = Comment.get_by_id(comment_id)
        if comment is None:
            return (
                jsonify(
                    {
                        "title": "There is no comment",
                        "msg": "Comment could not updated to db",
                    }
                ),
                400,
            )
        comment.body = body
        try:
            comment.save()
            return (
                jsonify({"title": "Comment updated", "msg": "Comment updated to db"}),
                200,
            )
        except Exception as error:
            db.session.rollback()
            return jsonify({"title": "save failed", "msg": str(error)}), 400
    else:
        comment = Comment.get_by_id(comment_id)
        if comment is None:
            return (
                jsonify({"title": "There is no comment", "msg": "No comment found"}),
                400,
            )
        return jsonify(Comment.__schema__().dump(comment)), 200


@app.route("/comment", methods=["POST"])
@jwt_required()
def add_comment():
    try:
        data = request.get_json(force=True)
    except Exception as error:
        return jsonify({"title": "request failed", "msg": str(error)}), 400
    body = data.get("body")
    user_id = data.get("user_id")
    post_id = data.get("post_id")
    if not body or not post_id or not user_id:
        return (
            jsonify(
                {
                    "title": "Comment failed",
                    "msg": "body,user_id and post_id are required",
                }
            ),
            400,
        )
    comment = Comment(body=body, user_id=user_id, post_id=post_id)
    try:
        comment.save()
        return (
            jsonify({"title": "Comment saved", "msg": "Comment saved to database"}),
            200,
        )
    except Exception as error:
        db.session.rollback()
        return jsonify({"title": "save failed", "msg": str(error)}), 400


# Get all comments from db
@app.route("/comments", methods=["GET"])
@jwt_required()
def manage_comments():
    comments = Comment.get_all()
    return jsonify(Comment.__schema__(many=True).dump(comments)), 200


# Authentication method for username and password
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
