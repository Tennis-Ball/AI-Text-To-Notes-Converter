from app import app
from flask import render_template, request, redirect, url_for


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html.j2")

