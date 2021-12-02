from wtforms.validators import Length, Regexp
import json

def write_json(form):

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


def validations(form):
    if form.year.data is not None:
        if int(form.year.data) <= 2015:
            form.serial.validators = [Regexp('^[A-Z]{2}'), Length(min=2, max=2)]
            form.number_doc.validators = [Regexp('^[0-9]{6}'), Length(min=6, max=6)]
        else:
            form.serial.validators = [Regexp('^[A-Z]{1}[1-9]{2}'), Length(min=3, max=3)]
            form.number_doc.validators = [Regexp('^[0-9]{8}'), Length(min=8, max=8)]