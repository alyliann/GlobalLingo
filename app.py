import git
from forms import InputForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request
from googletrans import Translator

app = Flask(__name__)
translator_obj = Translator()
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '3f8742cae18a7f0af440fe7979f95617'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)

# # do we need this?
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"

# with app.app_context():
#     db.create_all()

@app.route("/")
def home():
    # initialize form object from forms.py
    # pass in to render_template (look at Codio module)
    # create submit field in a form.py that, when pressed, redirects to /translator
    return render_template('home.html', subtitle='Translator', text='Welcome to translator!')

@app.route("/translator", methods= ['GET','POST'])
# need form object with stringfield for text input and stringfield for desired language input
# need submit button to, when pressed, generate translated text
def translator():
    if request.method == 'POST':
        original_text = request.form['original-text']
        translated_text = request.form['translated-text']
        result = translator_obj.translate(original_text, dest=translated_text)
        translated = result.text
        #add pronunciation
        return render_template('translator.html', title='Translator', final_translation = translated)
    else:
        return render_template("translator.html")

# remove this: not doing registration form?
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = InputForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

# leave this alone: connects to pythonanywhere
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/babynameoriginfinder/SEO-Week-3')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
