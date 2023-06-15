from app import app
from flask import jsonify, request
from app.models import User, Post

# Create, Update, Get, Delete one post from db

@app.route('/post/<post_id>', methods =['GET'])
def manage_post(post_id):
    post = Post.query.get(post_id)
    return jsonify({ 
     'body':post.body , 
     'timestamp':post.timestamp,
     'user_id':post.user_id
    }), 200



# Create, Update, Get, Delete one user from db
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json(force=True)
    username = data["username"]
    password = data["password"]
    user = User(username=username)
    user.set_password(password)
    user.save()
    return jsonify({"title": "User saved", "msg": "User saved to db"}), 201


@app.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    if request.method == "PUT":
        data = request.get_json(force=True)
        username = data["username"]
        password = data["password"]
        user = User.query.get(user_id)
        user.username = username
        user.password = password
        user.save()
        return jsonify({"title": "User updated", "msg": "User updated to db"}), 200

    elif request.method == "DELETE":
        user = User.query.get(user_id)
        user.delete()
        return jsonify({"title": "User deleted", "msg": "User deleted from db"}), 204

    else: # request.method == "GET"
        user = User.query.get(user_id)
        return jsonify({
            "username": user.username,
            "password": user.password_hash
        }), 200


# Get all user from db
@app.route('/users', methods=['GET'])
def manage_users():
    users = User.query.all()
    return jsonify([{'name': user.username, "id": user.id} for user in users]), 200

@app.route('/login', methods=['POST'])
def login(request):
    data = request.get_json(force=True)
    users = User.query.all()
    for user in users:
        if (
            user.username == data["username"]
            and user.password == data["password"]
        ):
            return jsonify({"title": "user logged in", "msg": "user logged in logged in successfully"}), 200
    # no user found with correct credentials
    return jsonify({"title": "invalid login", "msg": "invalid username or password"}), 400
