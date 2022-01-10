from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class AddFilmForm(FlaskForm):
    name_film = StringField('Name film', validators=[InputRequired(), Length(min=2, max=60)])
    director = StringField('Director', validators=[InputRequired(), Length(min=2, max=60)])
    release_date = StringField('Release_date', validators=[InputRequired(), Length(min=2, max=60)])
    info = TextAreaField('About film', validators=[Length(max=2000)])
    duration = StringField('Duratiion', validators=[InputRequired(), Length(min=2, max=60)])
    budget = StringField('Budget', validators=[InputRequired(), Length(min=2, max=100)])
    picture = FileField('Add  Poster Picture', validators=[FileAllowed(['jpg', 'png'])])
    category = SelectField(u'Category', coerce=int)
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    name = StringField('Genre name', validators=[DataRequired(), Length(min=0, max=100)])
    submit = SubmitField('')
