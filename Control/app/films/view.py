from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .forms import AddFilmForm, CategoryForm
from .models import Categoryfilm, Films
from .. import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from . import film_blueprint
from PIL import Image


@film_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_film():
    film = Films.query.order_by(Films.name_film).all()
    return render_template('view_film.html', films=film)


@film_blueprint.route('/addfilm', methods=['GET', 'POST'])
@login_required
def add_film():
    form = AddFilmForm()
    form.category.choices = [(category.id, category.genre) for category in Categoryfilm.query.all()]
    if form.validate_on_submit():
        film = Films(name_film=form.name_film.data, director=form.director.data, 
                    release_date=form.release_date.data, info=form.info.data,
                    duration=form.duration.data, budget=form.budget.data,
                    category_film=form.category.data, user_id=current_user.id)
        
        db.session.add(film)
        db.session.commit() 
        flash('Your film has been add!', category='success')
        return redirect(url_for('film.view_film'))
    
    return render_template('film_create.html', form=form)


@film_blueprint.route('/<id>', methods=['GET', 'POST'])
def detail_film(id):
    film = Films.query.get_or_404(id)
    return render_template('film_detail.html', pk=film)


@film_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
def delete_film(id):
    film = Films.query.get_or_404(id)
    if current_user.id == film.user_id:
        db.session.delete(film)
        db.session.commit()
        return redirect(url_for('film.view_film'))

    flash('This is not your post', category='warning')
    return redirect(url_for('film.detail_film', pk=id))


@film_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
def edit_film(id):
    film = Films.query.get_or_404(id)
    if current_user.id != film.user_id:
        flash('This is not your post', category='warning')
        return redirect(url_for('film.detail_film', pk=film))

    form = AddFilmForm()
    form.category.choices = [(category.id, category.genre) for category in Categoryfilm.query.all()]

    if form.validate_on_submit():
        film.name_film = form.name_film.data
        film.director = form.director.data
        film.release_date = form.release_date.data
        film.info = form.info.data
        film.duration = form.duration.data
        film.budget = form.budget.data
        film.category_film = form.category.data

        db.session.add(film)
        db.session.commit()

        flash('Film has been update', category='access')
        return redirect(url_for('film.detail_film', id=id))

        form.name_film.data = film.name_film
        form.director.data = film.director
        form.release_date.data = film.release_date
        form.info.data = film.info
        form.duration.data = film.duration
        form.budget.data = film.budget
        form.category.data = film.category_film 
    

    return render_template('film_create.html', form=form)


@film_blueprint.route('/categoryrcrud', methods=['GET', 'POST'])
def category_crud():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Categoryfilm(genre=form.name.data)

        db.session.add(category)
        db.session.commit()
        flash('Категорія добавленна')
        return redirect(url_for('.category_crud'))

    categories = Categoryfilm.query.all()
    return render_template('category_crud.html', categories=categories, form=form)


@film_blueprint.route('/update_category/<id>', methods=['GET', 'POST'])
def update_category(id):
    category = Categoryfilm.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.genre = form.name.data

        db.session.add(category)
        db.session.commit()
        flash('Категорія відредагована')
        return redirect(url_for('.category_crud'))

    form.name.data = category.genre
    categories = Categoryfilm.query.all()
    return render_template('category_crud.html', categories=categories, form=form)


@film_blueprint.route('/delete_category/<id>', methods=['GET'])
@login_required
def delete_category(id):
    category = Categoryfilm.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash('Category delete', category='access')
    return redirect(url_for('.category_crud'))
