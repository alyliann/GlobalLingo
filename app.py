
import git
import requests
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request
from googletrans import Translator

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
translator = Translator()
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '3f8742cae18a7f0af440fe7979f95617'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
@@ -23,13 +26,22 @@ def __repr__(self):
with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
@app.route("/home")
def about():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page', text='This is the about page')

@app.route("/translator", methods= ['GET','POST'])
def translator():
    if request.method == 'POST':
        original_text = request.form['original-text']
        translated_text = request.form['translated-text']
        result = translator.translate(original_text, dest=translated_text)
        translated = result.text
        return render_template('translator.html', title='Translator', final_translation = translated)
    else:
        return render_template("translator.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
