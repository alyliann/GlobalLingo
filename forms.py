import googletrans
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, AnyOf

valid_inputs = googletrans.LANGUAGES
languages = list(valid_inputs.keys()) + list(valid_inputs.values())

class TranslateForm(FlaskForm):
    text_input = TextAreaField('Enter text to translate',
                               validators=[DataRequired(), Length(min=1, max=10000)])
    language = StringField('Enter a language to translate to',
                           validators=[DataRequired(), AnyOf(languages,f"Please enter one of the following languages or its language code: {list(valid_inputs.values())}")])
    translate_text = SubmitField('Translate')
