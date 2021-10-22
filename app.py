from flask import Flask, render_template, request
from datetime import datetime, date
import sys
import os
app = Flask(__name__)
menu = {'Головна':'/', 'Коротка інформація':'/info', 'Мої досягнення':'/achievement'}
today = date.today()
age = today.year - 2002 - ((today.month, today.day) < (8, 20))
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

if __name__=='__main__':
    app.run(debug=True)