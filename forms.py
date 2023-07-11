from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class HomeForm(FlaskForm):
    redirect_button = Button('Go To Translate')

class TranslateForm(FlaskForm):
    text_input = TextAreaField('Enter text to translate')
    language = StringField('Enter a language to translate to')
    translate_text = Button('Translate')
