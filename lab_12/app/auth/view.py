from flask import url_for, render_template, flash, redirect, abort, current_app
from .. import db, bcrypt
from .forms import SignUpForm, LoginForm, UpdateAccountForm, ResetPasswordForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
from . import auth_blueprint
import os
import secrets
from PIL import Image
from datetime import datetime

@auth_blueprint.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('portfolio'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !', category='success')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form_reg=form, title='Register')


@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form_log = LoginForm()
    if form_log.validate_on_submit():
        user = User.query.filter_by(email=form_log.email.data).first()
        if user and user.verify_password(form_log.password.data):
            login_user(user, remember=form_log.remember.data)
            flash(f'You have been logged by username {user.email}!', category='success')
            return redirect(url_for('auth.account'))
        else:
            flash('Invalid login or password!', category='warning')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form_log=form_log, title='Login')


@auth_blueprint.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    all_users = User.query.all()
    count = User.query.count()
    if count == 0:
        abort(404)
    return render_template('auth/user_list.html', all_users=all_users, count=count)


@auth_blueprint.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))


@auth_blueprint.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form_acc = UpdateAccountForm()
    if form_acc.validate_on_submit():
        if form_acc.picture.data:
            picture_file = save_picture(form_acc.picture.data)
            current_user.image_file = picture_file
        current_user.username = form_acc.username.data
        current_user.email = form_acc.email.data
        current_user.about_me = form_acc.about_me.data
        db.session.commit()
        flash('Your account has been update!', category='success')
        return redirect(url_for('auth.account'))

    form_acc.about_me.data = current_user.about_me
    form_acc.username.data = current_user.username
    form_acc.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('auth/account.html', image_file=image_file, form_acc=form_acc, title='Account')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (400, 400)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@auth_blueprint.route("/reset-password", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.new_password1.data).decode('utf-8')
        db.session.commit()
        flash('Password changed', category='success')
        return redirect(url_for('auth.account'))
    return render_template('auth/reset password.html', form=form)


@auth_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_date = datetime.utcnow()
        db.session.commit()    