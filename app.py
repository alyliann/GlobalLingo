import git
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request
from googletrans import Translator

app = Flask(__name__)
translator_obj = Translator()
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '3f8742cae18a7f0af440fe7979f95617'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()

@app.route("/home")
def about():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')


@app.route("/translator", methods= ['GET','POST'])
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


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

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
