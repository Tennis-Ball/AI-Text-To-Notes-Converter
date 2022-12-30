from app import app
from flask import render_template, request, redirect, url_for


@app.route("/", methods=("GET"))
def test_page():
    return render_template("test.html.js")

