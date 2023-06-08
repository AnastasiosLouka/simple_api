from app import app
from flask import jsonify, request

from app.models import User


@app.route('/post')
def manage_post():
    return jsonify([
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]), 200


# Create, Update, Get, Delete one user from db
@app.route('/user/<user_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    if request.method == "POST":
        data = request.get_json(force=True)
        username = data["username"]
        password = data["password"]
        user = User(username=username, password=password)
        user.save()
        return jsonify({"title": "User saved", "msg": "User saved to db"}), 201

    elif request.method == "PUT":
        data = request.get_json(force=True)
        username = data["username"]
        password = data["password"]
        user = User.query.first(user_id)
        user.username = username
        user.password = password
        user.save()
        return jsonify({"title": "User updated", "msg": "User updated to db"}), 200

    elif request.method == "DELETE":
        user = User.query.first(user_id)
        user.delete()
        return jsonify({"title": "User deleted", "msg": "User deleted from db"}), 204

    else: # request.method == "GET"
        user = User.query.first(user_id)
        return jsonify({
            "username": user.username,
            "password": user.password
        }), 200


# Get all user from db
@app.route('/users', methods=['GET'])
def manage_users():
    users = User.get.all()
    return jsonify({'name': user.username for user in users}), 200


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
