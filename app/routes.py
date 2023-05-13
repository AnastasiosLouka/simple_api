from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, jsonify

@app.route('/')
@app.route('/index')
def index():
    title='Home'
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title=title, user=user, posts=posts)
    # return jsonify({
    #     "title": title,
    #     "username": user['username'],
    #     "posts": posts
    # }), 200

@app.route('/contact')
def contact():
    return render_template('contact.html')
   


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)