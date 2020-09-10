from flask import Flask, render_template, request
from flask import send_file, url_for, redirect

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")
