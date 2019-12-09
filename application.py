import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    """Redirect index page to /form route"""
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    """Return empty form if get request is made"""
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    messages = []
    # checking for valid inputs via form
    if not request.form.get('first_name'):
        messages.append('Please write your name')
        return render_template('error.html', messages=messages)
    elif not request.form.get('last_name'):
        messages.append('Please write your last name')
        return render_template('error.html', messages=messages)
    elif not request.form.get('email'):
        messages.append('Please write your email')
        return render_template('error.html', messages=messages)
    else:
        with open('survey.csv', 'a') as file:
            writer = csv.writer(file)
        return redirect('/sheet')
    return render_template("form.html")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    """Read from csv file and retrieve users"""
    with open('survey.csv', 'r') as file:
        reader = csv.reader(file)
        users = list(reader)
    return render_template("sheets.html", users=users)
