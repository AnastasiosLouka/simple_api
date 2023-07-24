from app import app, db
from flask import jsonify, request
from app.models import User, Post


# Create, Update, Get, Delete one post from db
@app.route("/post/<post_id>", methods=["GET", "PUT", "DELETE"])
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
        return (
            jsonify(
                {
                    "body": post.body,
                    "timestamp": post.timestamp,
                    "user_id": post.user_id,
                    "id": post.id,
                }
            ),
            200,
        )


@app.route("/post", methods=["POST"])
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
def manage_posts():
    posts = Post.get_all()
    return (
        jsonify(
            [
                {
                    "body": post.body,
                    "user_id": post.user_id,
                    "id": post.id,
                    "time": post.timestamp,
                }
                for post in posts
            ]
        ),
        200,
    )

# Create, Update, Get, Delete one user from db
@app.route("/user", methods=["POST"])
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

        return (
            jsonify(
                {
                    "name": user.username,
                    "id": user.id,
                    "password": user.password_hash,
                    "posts": [
                        {
                            "body": post.body,
                            "post_id": post.id,
                            "user_id": post.user_id,
                            "time": post.timestamp,
                        }
                        for post in user.posts
                    ],
                }
            ),
            200,
        )


# Get all user from db
@app.route("/users", methods=["GET"])
def manage_users():
    users = User.get_all()
    return (
        jsonify(
            [
                {
                    "name": user.username,
                    "id": user.id,
                    "password": user.password_hash,
                    "posts": [
                        {
                            "body": post.body,
                            "post_id": post.id,
                            "user_id": post.user_id,
                            "time": post.timestamp,
                        }
                        for post in user.posts
                    ],
                }
                for user in users
            ]
        ),
        200,
    )
