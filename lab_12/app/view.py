from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from datetime import datetime, date
import sys, os, platform, json
from flask import current_app as app
            
today = date.today()
age = today.year - 2002 - ((today.month, today.day) < (8, 20))
@app.route("/")
def home():
    return render_template('index.html', my_os=os.uname(),
                           user_agent=request.headers.get('User-Agent'), version=sys.version,
                           time_now=datetime.now().strftime("%H:%M"))

@app.route("/info")
def info():
    return render_template('info.html', age=age, month=today.month, day=today.day)

@app.route("/achievement")
def achievement():
    return render_template('achievement.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
