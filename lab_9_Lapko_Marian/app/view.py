from flask import Flask, render_template, request, redirect, url_for, flash, session, url_for 
from datetime import datetime, date
import sys
import os
from app import app, db
from app.forms import ContactForm
import json
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError 
import email_validator
from .forms import DataForm, SignUpForm, LoginForm
from .function import write_json, validations
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
#app = Flask(__name__)
"""
menu = {'Головна':'/', 'Info':'/info', 'Achivment':'/achievement', 
        'Contact':'/contact', 'Register Cabinet':'/register_cabinet', 
        'SignUp':'/SignUp', 'LogIn':'/LogIn', 'LogOut':'/logout', 'Account':'/account', 'Users':'/users'}
menu1= {'Головна':'/', 'Info':'/info', 'Achivment':'/achievement', 
        'Contact':'/contact', 'Register Cabinet':'/register_cabinet', 
        'LogOut':'/logout', 'Account':'/account', 'Users':'/users'}  
"""             
today = date.today()
age = today.year - 2002 - ((today.month, today.day) < (8, 20))
@app.route("/")
def index():
    return render_template('index.html', my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))

@app.route("/info")
def info():
    return render_template('info.html', age=age, month=today.month, day=today.day)

@app.route("/achievement")
def achievement():
    return render_template('achievement.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    cookie_name = session.get("name")
    cookie_email = session.get("email")
    print(cookie_email,cookie_name)
    if request.method == 'POST':
        if cookie_name is None and cookie_email is None: # якщо кукі не встановлено, тобто ми перший раз відкрили сторінку
            if form.validate_on_submit():
                name = form.name.data
                email = form.email.data
                body = form.body.data
                session['name'] = name
                session['email'] = email
                with open('data.txt', 'a') as outfile:
                    json.dump({'name': session.get("name"), 'email': session.get("email"), 'body': body}, outfile)
                    outfile.write('\n')
                flash(message='Повідомлення надіслано успішно!')
                return redirect(url_for('contact'))
            else:
                flash(message='Помилка відправки повідомлення!')
        else: # якщо вхід на сторіку здійснено повторно
            form.name.data = cookie_name # встановлюємо значення для форми name та email
            form.email.data = cookie_email
            if form.validate_on_submit():
                body = form.body.data
                with open('data.txt', 'a') as outfile:
                    json.dump({'name': session.get("name"), 'email': session.get("email"), 'body': body}, outfile)
                    outfile.write('\n')
                flash(message='Повідомлення надіслано успішно!')
                return redirect(url_for('contact'))
            else:
                flash(message='Помилка відправки повідомлення!')
    return render_template('contact_form.html', form=form, cookie_name=session.get("name"), 
                            cookie_email=session.get("email"))


@app.route("/register_cabinet", methods=['GET', 'POST'])
def register_cabinet():

    form = DataForm()
    validations(form)
    if form.validate_on_submit():
        session['email'] = form.email.data
        write_json(form)
        flash('User has been written in json file')
        return redirect(url_for('register_cabinet'))

    try:
        ses = session['email']
    except:
        return render_template('start.html', form=form)

    with open('data.json') as f:
        data_files = json.load(f)

    return render_template('start.html', menu=menu, form=form, email=ses, number=data_files[ses]['number'], year=data_files[ses]['year'], 
                            pin=data_files[ses]['pin'], serial=data_files[ses]['serial'], number_doc=data_files[ses]['number_doc'])



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !', category='success')
        return redirect(url_for('login'))
    return render_template('signup.html', form_reg=form, title='Register')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_log = LoginForm()
    if form_log.validate_on_submit():
        user = User.query.filter_by(email=form_log.email.data).first()
        if user and user.verify_password(form_log.password.data):
            login_user(user, remember=form_log.remember.data)
            flash(f'You have been logged by username {user.email}!', category='success')
            return redirect(url_for('login'))
        else:
            flash('Invalid login or password!', category='warning')
            return redirect(url_for('login'))

    return render_template('login.html', form_log=form_log, title='Login')


@app.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    all_users = User.query.all()
    count = User.query.count()
    if count == 0:
        return render_template('404.html')
    return render_template('user_list.html', all_users=all_users, count=count)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')
