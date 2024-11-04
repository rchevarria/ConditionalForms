from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, BooleanField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Optional
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_form_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    class DynamicForm(FlaskForm):
        pass

    for field in data['fields']:
        field_name = field['name']
        field_type = field['type']
        field_label = field['label']
        required = field.get('required', False)
        choices = field.get('choices', [])
        conditional = field.get('conditional', None)

        if field_type == 'StringField':
            setattr(DynamicForm, field_name, StringField(field_label, validators=[DataRequired() if required else Optional()]))
        elif field_type == 'EmailField':
            setattr(DynamicForm, field_name, EmailField(field_label, validators=[DataRequired() if required else Optional()]))
        elif field_type == 'IntegerField':
            setattr(DynamicForm, field_name, IntegerField(field_label, validators=[Optional()]))
        elif field_type == 'RadioField':
            setattr(DynamicForm, field_name, RadioField(field_label, choices=[(choice, choice) for choice in choices], validators=[Optional()]))
        elif field_type == 'SelectField':
            setattr(DynamicForm, field_name, SelectField(field_label, choices=[(choice, choice) for choice in choices], validators=[Optional()]))

        if conditional:
            setattr(DynamicForm, f"{field_name}_conditional", conditional)

    return DynamicForm()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = create_form_from_json('form_config.json')
    if request.method == 'POST' and form.validate_on_submit():
        return 'Form submitted successfully!'
    return render_template('form_template.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
