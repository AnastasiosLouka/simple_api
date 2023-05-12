from app import app
from flask import render_template

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

@app.route('/contact')
def contact():
    return render_template('contact.html')