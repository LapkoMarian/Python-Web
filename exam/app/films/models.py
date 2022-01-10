import enum

from .. import db


class Categoryfilm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50), nullable=False)
    film = db.relationship('Films', backref='category', lazy=True)


class Films(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_film = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String(50), nullable=False)
    info = db.Column(db.Text, nullable=True)
    duration = db.Column(db.String(50), nullable=False)
    budget = db.Column(db.String(50), nullable=False)   
    category_film = db.Column(db.Integer, db.ForeignKey('categoryfilm.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    def __repr__(self):
        return f"Post('{self.id}', '{self.name_film}')"
