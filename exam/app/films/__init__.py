from flask import Blueprint

film_blueprint = Blueprint('film', __name__, template_folder="templates/films")

from . import view
