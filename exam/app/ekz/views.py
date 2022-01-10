from flask import Flask, g, request, jsonify
from functools import wraps
from ..films.models import Films
from .. import db

from . import api_blueprint

api_username = 'admin'
api_password = 'password'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated


@api_blueprint.route('/films', methods=['GET'])
@protected
def get_films():
    films = Films.query.all()
    return_values = [{"id": films.id,
                      "name_film": films.name_inst,
                      "director": films.director,
                      "release_date": films.count_student,
                      "info": films.info,
                      "duration": films.duration,
                      "budget": films.budget,
                      "category_film": films.category_film} for film in films]

    return jsonify({'Film': return_values})


@api_blueprint.route('/film/<int:id>', methods=['GET'])
@protected
def get_film(id):
    film = Film.query.get_or_404(id)
    return jsonify({"id": films.id,
                    "name_film": films.name_inst,
                    "director": films.director,
                    "release_date": films.count_student,
                    "info": films.info,
                    "duration": films.duration,
                    "budget": films.budget,
                    "category_film": films.category_film})


@api_blueprint.route('/film', methods=['POST'])
def add_film():
    new_film_data = request.get_json()
    film = Films.query.filter_by(name_film=new_film_data['name_film']).first()

    if film:
        return jsonify({"Message": "Category already exist"})

    film = Films(
        name_film=new_film_data['name_film'],
        director=new_film_data['director'],
        release_date=new_film_data['release_date'],
        info=new_film_data['info'],
        duration=new_film_data['duration'],
        budget=new_film_data['budget'],
        category_film=new_film_data['category_film'],
        user_id=new_film_data['user_id']
    )
    print(new_film_data['name_film'])
    print(new_film_data['name_film'])
    db.session.add(film)
    db.session.commit()
    return jsonify({"id": film.id,
                    "name_film": film.name_inst,
                    "director": film.director,
                    "release_date": film.count_student,
                    "info": film.info,
                    "duration": film.duration,
                    "budget": film.budget,
                    "category_film": film.category_film})


@api_blueprint.route('/film/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit_film(id):
    film = Films.query.get(id)
    if not films:
        return jsonify({"Message": "Category does not exist"})

    update_category_data = request.get_json()
    films = Films.query.filter_by(name_film=update_category_data['name_film']).first()
    if films:
        return jsonify({"Message": "Category already exist"})

    film.name_film = update_category_data['name_inst']
    film.director = update_category_data['director']
    film.release_data = update_category_data['release_data']
    film.info = update_category_data['info']
    film.duration = update_category_data['duration']
    film.budget = update_category_data['budget']
    film.category_film = update_category_data['category_film']
    film.user_id = update_category_data['user_id']

    db.session.add(films)
    db.session.commit()

    return jsonify({"id": film.id,
                    "name_film": film.name_inst,
                    "director": film.director,
                    "release_date": film.count_student,
                    "info": film.info,
                    "duration": film.duration,
                    "budget": film.budget,
                    "category_film": film.category_film})


@api_blueprint.route('/film/<int:id>', methods=['DELETE'])
@protected
def delete_film(id):
    films = Films.query.get_or_404(id)
    db.session.delete(films)
    db.session.commit()

    return jsonify({'Message': 'The category has been deleted!'})
