import googletrans
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, AnyOf

# class HomeForm(FlaskForm):
#     redirect_button = SubmitField('Go To Translate')

# valid_inputs = googletrans.LANGUAGES
# langcodes = valid_inputs.keys()
# languages = valid_inputs.values()
# valid_inputs = langcodes + languages

valid_inputs = googletrans.LANGUAGES
languages = list(valid_inputs.keys()) + list(valid_inputs.values())

class TranslateForm(FlaskForm):
    text_input = TextAreaField('Enter text to translate',
                               validators=[DataRequired(), Length(min=1, max=10000)])
    language = StringField('Enter a language to translate to',
                           validators=[DataRequired(), AnyOf(languages)])
    translate_text = SubmitField('Translate')
