
from app import app

from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_user, logout_user

from .auth.forms import SignUpForm, LoginForm
from .models import User

@app.route('/')
def homePage():
    users = User.query.all()
    # users = User.query.limit(20)
    follow_set = set()

    if current_user.is_authenticated:
        users_following = current_user.following.all()
        print(users_following)
        for u in users_following:
            follow_set.add(u.id)
        for u in users:
            if u.id in follow_set:
                u.flag = True

    

    return render_template('index.html', users=users)



