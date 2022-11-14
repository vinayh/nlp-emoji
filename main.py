import os

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_assets import Bundle, Environment

app = Flask(__name__)
if 'SECRET_KEY' in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
else:
    raise Exception
assets = Environment(app)
assets.url = app.static_url_path

# Scss files
scss = Bundle(
    "assets/main.scss",
    filters="libsass",
    output="css/scss-generated.css"
)
assets.register("scss_all", scss)

# JS files
js = Bundle(
    "assets/node_modules/jquery/dist/jquery.min.js",
    "assets/node_modules/@popperjs/core/dist/umd/popper.min.js",
    "assets/node_modules/bootstrap/dist/js/bootstrap.min.js",
    filters="jsmin",
    output="js/generated.js"
)
assets.register("js_all", js)


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        description = request.form['description']
        # info = request.form['info']

        if not description:
            flash('Description is required!')
        # elif not info:
        #     flash('More info is required!')
        else:
            # TODO: Add action using form submission here
            # messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')
