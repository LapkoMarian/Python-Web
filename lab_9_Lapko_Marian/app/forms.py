from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, TextAreaField, BooleanField, SelectField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Optional, InputRequired, EqualTo, Regexp, DataRequired, ValidationError
from datetime import datetime
from .models import User


class ContactForm(FlaskForm):
    name = StringField(
            'Name',
            validators=[DataRequired(message="Поле не можу бути пустим!")],
            render_kw={'size':31}
        )
    email = StringField(
            'Email',
            validators=[
                DataRequired(),
                Email(message='Incorrect email address!')
            ],
            render_kw={'size': 31}
        )
    body = TextAreaField(
            'Body',
            validators=[
                DataRequired(),
                Length(min=1, max=150, message="Field must be between 1 and 150 characters long!")
            ],
            render_kw={'cols':35, 'rows': 5}
        )
    submit = SubmitField('Submit')

class DataForm(FlaskForm):
    email = StringField(
            'Email*', 
            validators=[InputRequired('Email is required'), Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'), 
            Length(min=5, max=30, message='Must be at least 5 and at most 10 characters')])
    password1 = PasswordField(
            'Password*', validators=[InputRequired('Password is required'), Length(min=6, message='Must be at least 6')])
    password2 = PasswordField(
            'Repeat the password*', validators=[InputRequired('Password is required'), 
            Length(min=6, message='Must be at least 6'), EqualTo('password1')])

    number = StringField(
            'Number*', validators=[InputRequired('Number is required'), Regexp('[0-9]{7}', 
                message='Must be numbers'), Length(min=7, max=7)])
    pin = StringField(
            'Pin code*', validators=[InputRequired('Pin code is required'), Regexp('[0-9]{4}', 
                message='Must be numbers'), Length(min=4, max=4)])
    year = SelectField(
            'Year*', choices=[('2020', '2020'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), 
                              ('2016', '2016'), ('2015', '2015'), ('2014', '2014'), ('2013', '2013')])
    serial = StringField('Serial number')
    number_doc = StringField('Number document*')
    submit = SubmitField(label=('Submit'))

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('A username is required'), Length(min=4, max=14, message='Name must have greater 4 symbol and least 14 symbol'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dots or underscores')])
    email = StringField('Email', validators=[InputRequired('Email is required'),Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='Invali Email')])
    password1 = PasswordField('Password', validators=[InputRequired('Password is required'), Length(min=6, message='Must be at least 6')])
    password2 = PasswordField('Repeat the password', validators=[InputRequired('Password is required'),Length(min=6, message='Must be at least 6'), EqualTo('password1')])
    submit = SubmitField(label=(''))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired() ,Regexp('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('')
    submit = SubmitField(label=(''))

