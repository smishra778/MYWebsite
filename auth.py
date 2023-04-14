from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong UserId or Password', category='error')
        else:
            flash('User Not Found', category='error')

    return render_template("LoginPage.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login') )


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        terms_and_conditions = request.form.get('on')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists! Please use a different email', category='error')
        elif len(email) < 4:
            flash('Email must at least have 5 characters', category='error')
        elif len(full_name) < 4:
            flash('Full Name must at least have 2 characters', category='error')
        elif len(password) < 7:
            flash('Password must at least have 7 characters', category='error')
        else:
            # add user to the database
            new_user = User(email=email, full_name=full_name,
                            password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account Created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)
