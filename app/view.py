from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date
import sys
import os
from app import app
from app.forms import ContactForm
import json
# app = Flask(__name__)
menu = {'Головна':'/', 'Коротка інформація':'/info', 'Мої досягнення':'/achievement', 'Contact':'/contact'}
today = date.today()
age = today.year - 2001 - ((today.month, today.day) < (4, 14))
@app.route('/')
def index():
    return render_template('index.html', menu=menu, my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))

@app.route('/info')
def info():
    return render_template('info.html', menu=menu,age=age, month=today.month, day=today.day)

@app.route('/achievement')
def achievement():
    return render_template('achievement.html', menu=menu)

@app.route('/contact', methods=["GET", "POST"])
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
    return render_template('contact_form.html', menu=menu, form=form, cookie_name=session.get("name"), cookie_email=session.get("email"))