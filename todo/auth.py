from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    print(user)

    if not user:
        if not check_password_hash(user.password, password):
            flash('Bitte überprüfen Sie Ihre Zugangsdaten und versuchen Sie es erneut...')
            return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))


    return render_template('auth/login.html')

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    user = User.query.filter_by(username=username).first()

    if user:
        # CAN'T REGISTER BECAUSE USER ALREADY IN DB
        flash('Benutzer existiert bereits...')
        return redirect(url_for('auth.signup'))
    else:
        # REGISTER NEW USER
        new_user = User(name=name, username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Benutzer {new_user.username} Erfolgreich registriert...')
        return redirect(url_for('auth.login'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))