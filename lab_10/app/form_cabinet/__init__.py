from flask import Blueprint, render_template, flash, session, redirect, url_for, request
from .forms import DataForm, ContactForm
from .function import validations, write_json
import json

cabinet_blueprint = Blueprint('cabinet', __name__, template_folder="templates/form_cabinet")


@cabinet_blueprint.route("/contact_form", methods=['GET', 'POST'])
def contact_form():
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
                return redirect(url_for('cabinet.contact_form'))
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
                return redirect(url_for('cabinet.contact_form'))
            else:
                flash(message='Помилка відправки повідомлення!')
    return render_template('contact_form.html', form=form, cookie_name=session.get("name"), 
                            cookie_email=session.get("email"))



@cabinet_blueprint.route("/register_cabinet", methods=['GET', 'POST'])
def register_cabinet():

    form = DataForm()
    validations(form)
    if form.validate_on_submit():
        session['email'] = form.email.data
        write_json(form)
        flash('User has been written in json file')
        return redirect(url_for('cabinet.register_cabinet'))

    try:
        sesiya = session['email']

    except:
        return render_template('start.html', form=form)

    with open('data.json') as f:
        data_files = json.load(f)

    form.email.data = session['email']
    form.number.data = data_files[sesiya]['number']
    form.pin.data = data_files[sesiya]['pin']
    form.year.data = data_files[sesiya]['year']
    form.serial.data = data_files[sesiya]['serial']
    form.number.data = data_files[sesiya]['number_doc']

    return render_template('start.html', form=form)