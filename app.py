from flask import Flask, render_template
from flask_assets import Bundle, Environment

app = Flask(__name__)
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


@app.route("/")
def index():
    return render_template("index.html")
