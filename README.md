![workflow test status badge](https://github.com/alyliann/SEO-Translator/actions/workflows/test.yaml/badge.svg)

# SEO-Project-2: GlobalLingo
SEO Tech Developer program project 2 created by Alysa Vega, Chinyere Amasiatu, and Myah Jackson-Solomon.

## Setup instructions

#### Libraries to install
* googletrans
```
pip install googletrans==4.0.0-rc1
```
* Flask-WTF
```
pip install Flask-WTF
```
* Flask-SQLAlchemy
```
pip install Flask-SQLAlchemy
```
* flask-behind-proxy
```
pip install flask-behind-proxy
```


## Running the code

To run `app.py` in a terminal, type:
```
python3 app.py
```

## How the code works

`app.py` and `forms.py` provide the backend for the GlobalLingo program, with the files in `templates` and `static` providing the frontend.
GlobalLingo takes a language and text as input, using the googletrans API to translate the user's text to the desired language.
