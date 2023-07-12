from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

# class HomeForm(FlaskForm):
#     redirect_button = SubmitField('Go To Translate')

class TranslateForm(FlaskForm):
    text_input = TextAreaField('Enter text to translate',
                               validators=[DataRequired(), Length(min=1, max=10000)])
    language = StringField('Enter a language to translate to',
                           validators=[DataRequired()])
    translate_text = SubmitField('Translate')
