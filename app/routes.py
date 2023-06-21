from app import app
from flask import jsonify, request
from app.models import User, Post


# Create, Update, Get, Delete one post from db
@app.route('/post/<post_id>', methods =['GET', 'PUT', 'DELETE'])
def manage_post(post_id):
    if request.method == 'GET':
        post = Post.query.get(post_id)
        if post == None :
            return jsonify({"msg": "there is no post"}), 400
        
        else :
            return jsonify({ 
            'body':post.body , 
            'timestamp':post.timestamp,
            'user_id':post.user_id
        }), 200
    
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        body = data.get("body")
        if body == None:
            return jsonify({"msg": "body is required"}), 400
        post = Post.query.get(post_id)
        if post == None:
            return jsonify({"title": "There is no post", "msg": "Post could not updated to db"}),400
        post.body = body
        post.save()
        return jsonify({"title": "Post updated", "msg": "Post updated to db"}), 200

    else: #if request.mehod == 'DELETE'
        post = Post.query.get(post_id)
        if post == None:
            return jsonify({"msg":"No post deleted"}), 400
        else: 
            post.delete()
            return jsonify({"title": "Post deleted", "msg": "Post deleted from db"}), 204
    

@app.route('/post', methods =['POST'])
def add_post():
    data = request.get_json(force=True)
    body = data["body"]
    user_id = data["user_id"] 
    if body == None:
        return jsonify({"msg": "body is required"}), 400 #1
    elif user_id == None:
        return jsonify({"msg":"user_id required"}), 400  #2
    else:
        post = Post(body=body, user_id=user_id)
        post.save()
    return jsonify({"title":"Post saved"}),201


# Get all posts from db
@app.route('/posts', methods=['GET'])
def manage_posts():
    posts = Post.query.all()
    return jsonify([{"body":post.body, "user_id":post.user_id, "id": post.id} for post in posts]), 200


# Create, Update, Get, Delete one user from db
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json(force=True)
    username = data.get("username")
    if username == None:
        return jsonify({"msg":"username is required"})
    password = data.get("password")
    if password == None:
        return jsonify({"msg":"password is required"})
    user = User(username=username)
    user.set_password(password)
    user.save()
    return jsonify({"title": "User saved", "msg": "User saved to db"}), 201


@app.route('/user/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    if request.method == "PUT":
        data = request.get_json(force=True)
        username = data["username"]
        if username == None:
            return jsonify({"msg":"username is required"})#3
        password = data["password"]
        if password == None:
            return jsonify({"msg":"password is required"})#4
        user = User.query.get(user_id)
        user.username = username
        user.set_password(password)
        user.save()
        return jsonify({"title": "User updated", "msg": "User updated to db"}), 200

    elif request.method == "DELETE":
        user = User.query.get(user_id)
        if user == None:
            return jsonify({"msg":"no user deleted"}),400
        else:
            user.delete()
        return jsonify({"title": "User deleted", "msg": "User deleted from db"}), 204

    else: # request.method == "GET"
        user = User.query.get(user_id)
        if user == None:
            return jsonify({"msg":"There in no user"}),400
        else:
            return jsonify({
            "username": user.username,
            "password": user.password_hash
        }), 200


# Get all user from db
@app.route('/users', methods=['GET'])
def manage_users():
    users = User.query.all()
    return jsonify([{'name': user.username, "id": user.id} for user in users]), 200

