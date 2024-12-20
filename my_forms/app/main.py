from flask import Flask, request, jsonify, make_response
from tinydb import TinyDB, Query
import re
from datetime import datetime
import logging
from functools import lru_cache
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger, swag_from

app = Flask(__name__)
db = TinyDB('templates.json')
auth = HTTPBasicAuth()
swagger = Swagger(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Пользователи для аутентификации
users = {
    "admin": generate_password_hash("admin_password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", phone)

def validate_date(date):
    formats = ["%d.%m.%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            datetime.strptime(date, fmt)
            return True
        except ValueError:
            continue
    return False

def determine_field_type(value):
    if validate_date(value):
        return "date"
    elif validate_phone(value):
        return "phone"
    elif validate_email(value):
        return "email"
    else:
        return "text"

@app.route('/get_form', methods=['POST'])
@auth.login_required
@swag_from({
    'tags': ['Form'],
    'summary': 'Get the form template name based on the provided form data',
    'parameters': [
        {
            'name': 'form_data',
            'in': 'formData',
            'description': 'Form data as key-value pairs',
            'required': True,
            'type': 'object'
        }
    ],
    'responses': {
        '200': {
            'description': 'Success'
        },
        '400': {
            'description': 'Bad Request'
        }
    }
})
def get_form():
    form_data = request.form.to_dict()
    form_fields = {key: determine_field_type(value) for key, value in form_data.items()}

    Template = Query()
    for template in db.all():
        template_fields = template['fields']
        if all(item in form_fields.items() for item in template_fields.items()):
            logging.info(f"Template found: {template['name']}")
            return jsonify({"name": template['name']})

    logging.warning(f"No matching template found. Returning field types: {form_fields}")
    return jsonify(form_fields)

@app.errorhandler(404)
def not_found(error):
    logging.error('Not found: %s', request.url)
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    logging.error('Server error: %s', str(error))
    return make_response(jsonify({'error': 'Internal server error'}), 500)

@lru_cache(maxsize=128)
def get_template_by_name(name):
    Template = Query()
    template = db.search(Template.name == name)
    return template[0] if template else None

if __name__ == '__main__':
    app.run(debug=True)
