from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import InputRequired, DataRequired, Length, AnyOf, Email, NumberRange, Regexp
import json, re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisSecretKey'


class LoginForm(FlaskForm):
    email = StringField('Email*', validators=[InputRequired('Email is required'), Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'), Length(min=5, max=30, message='Must be at least 5 and at most 10 characters')])
    password1 = PasswordField('Password*', validators=[InputRequired('Password is required'), Length(min=6, message='Must be at least 6')])
    password2 = PasswordField('Repeat the password*', validators=[InputRequired('Password is required'), Length(min=6, message='Must be at least 6')])

    # Дані екзаменаційного листка (сертифіката) ЄВІ/ЄФВВ - вказується для вступу до магістратури
    number = StringField('Number*', validators=[InputRequired('Number is required'), Regexp('[0-9]{7}', message='Must be numbers'), Length(min=7, max=7)])
    pin = StringField('Pin code*', validators=[InputRequired('Pin code is required'), Regexp('[0-9]{4}', message='Must be numbers'), Length(min=4, max=4)])
    year = SelectField('Year*', choices=[('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013')])
    serial = StringField('Serial number', validators=[Length(max=3, message='Must be at 2 symbols if year 2015 and least or must be 3 symbols if greater than 2015')])
    number_doc = StringField('Number document*', validators=[Length(min=6, max=8, message='Number document error')])

@app.route("/", methods=['GET', 'POST'])
def start():

    form = LoginForm()

    if form.validate_on_submit():

        if form.password1.data == form.password2.data:

            if int(form.year.data) <= 2015:
                if len(form.serial.data) > 2:
                    return render_template('start.html', form=form, serialerr='Serial error')

                if bool(re.search(r'^[A-Z]{2}', form.serial.data)) == False:
                    return render_template('start.html', form=form, serialerr='Serial error')

                if len(form.number_doc.data) > 6:
                    return render_template('start.html', form=form, numdocerror='Number document error')

            else:
                if bool(re.search(r'^[A-Z]{1}[1-9]{2}', form.serial.data)) == False:
                    return render_template('start.html', form=form, serialerr='Serial error')

                if len(form.number_doc.data) < 8:
                    return render_template('start.html', form=form, numdocerror='Number document error')



            data = {
                form.email.data: {
                    'password': form.password1.data,
                    'number': form.number.data,
                    'pin': form.pin.data,
                    'year': form.year.data,
                    'serial': form.serial.data,
                    'number_doc': form.number_doc.data,
                },
            }

            try:
                with open('data.json') as f:
                    data_files = json.load(f)
                    data_files.update(data)

                    with open('data.json', 'w', encoding='utf-8') as f:
                        json.dump(data_files, f, ensure_ascii=False, indent=4)
            except:
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            return f'The username is {form.email.data}. The password is {form.password1.data}'
        else:
            return render_template('start.html', form=form, error='Password did not much')

    return render_template('start.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)