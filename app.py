import git
from googletrans import Translator
from forms import TranslateForm#, HomeForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '3f8742cae18a7f0af440fe7979f95617'

'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()'''

@app.route("/")
def home():
    # home_form = HomeForm()
    # if home_form.validate_on_submit(): # change "validate_on_submit" function
    #     return redirect(url_for('translator')) # if so - send to translator page
    return render_template('home.html', text='Welcome to translator!')

@app.route("/translator", methods= ['GET','POST'])
def translator():
    form = TranslateForm()
    if form.validate_on_submit():
        translator_obj = Translator()

        language = parseLanguage(str(form.language))
        text_input = parseText(str(form.text_input))

        result = translator_obj.translate(text_input, dest=language)
        translated = result.text
        pronounced = result.pronunciation
        
        if pronounced == None:
            pronounced = translated

        return render_template('translator.html', title='Translator', final_translation=translated, final_pronunciation=pronounced, form=form)
    return render_template('translator.html', title='Translator', form=form)

def parseLanguage(language):
    # <input id="language" name="language" required type="text" value="fr">
    index = language.find('value')
    language = language[index+7:-2] # should be ' fr"> '
    return language

def parseText(text_input):
    # <textarea id="text_input" maxlength="10000" minlength="1" name="text_input" required>Hello</textarea>
    index = text_input.find('>')
    text_input = text_input[index+1:-11]
    return text_input


'''@app.route("/register", methods=['GET', 'POST'])
def register():
    form = InputForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)'''

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
