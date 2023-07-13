import git
import googletrans
from googletrans import Translator
from forms import TranslateForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request

app = Flask(__name__, static_folder='static')
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '3f8742cae18a7f0af440fe7979f95617'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang1 = db.Column(db.String(60), nullable=False)
    original_text = db.Column(db.String(10000), nullable=False)
    lang2 = db.Column(db.String(60), nullable=False)
    translated_text = db.Column(db.String(10000), nullable=False)
    pronunced_text = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f"Translation('{self.id}', '{self.lang1}', '{self.original_text}','{self.lang2}', '{self.translated_text}', '{self.pronunced_text}')"

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', text='Welcome to translator!')

@app.route("/translator", methods= ['GET','POST'])
def translator():
    form = TranslateForm()
    if form.validate_on_submit():
        
        translator_obj = Translator()

        lang_dict = googletrans.LANGUAGES

        language = parseLanguage(str(form.language))
        text_input = parseText(str(form.text_input))

        result = translator_obj.translate(text_input, dest=language)
        translated = result.text
        pronounced = result.pronunciation
        original_lang = lang_dict[result.src].capitalize()
        if language in lang_dict:
            translated_lang = lang_dict[language].capitalize()
        else:
            translated_lang = language.capitalize()
        if pronounced == None:
            pronounced = translated
        sentence = f"Translating {original_lang} -> {translated_lang}..."

        translation = Translation(lang1=original_lang, original_text=text_input, lang2=translated_lang, translated_text=translated, pronunced_text=pronounced)
        db.session.add(translation)
        db.session.commit()

        return render_template('translator.html', title='Translator', final_translation=translated,
                                final_pronunciation=pronounced,final_sentence = sentence, form=form)
    return render_template('translator.html', title='Translator', form=form)

def parseLanguage(language):
    index = language.find('value')
    language = language[index+7:-2]
    if language.lower() == 'chinese':
        language = 'chinese (simplified)'
    return language

def parseText(text_input):
    index = text_input.find('>')
    text_input = text_input[index+1:-11]
    return text_input

# leave this alone: connects to pythonanywhere
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/babynameoriginfinder/SEO-Translator')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
