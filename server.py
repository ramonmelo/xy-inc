
import os
import sqlite3
from flask import Flask, jsonify, request, render_template, redirect, url_for

from db_manager import DBManager

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'db.sqlite')
))

db = DBManager(app)

# Views

@app.route("/")
def index():
    return redirect(url_for('create'))

@app.route("/create/")
def create():
    return render_template('create.html')

@app.route("/find/")
def find():
    return render_template('find.html')

# API

@app.route("/create", methods=['POST'])
def create_poi():
    name = request.args.get('name', None)
    x = request.args.get('x', None)
    y = request.args.get('y', None)

    try:
        if name and x and y:
            x = int(x)
            y = int(y)

            db.create_poi(name, x, y)
            out = "Saved with success."

    except (AssertionError, TypeError):
        out = "Please, send valid values."

    return out

@app.route("/list", methods=['GET'])
def list_poi():
    x = request.args.get('x', None)
    y = request.args.get('y', None)
    distance = request.args.get('distance', None)

    try:
        if x and y and distance:
            x = int(x)
            y = int(y)
            distance = int(distance)

        out = jsonify( db.list_poi(x, y, distance) )
    except (AssertionError, TypeError):
        out = "Please, send valid values."

    return out

if __name__ == "__main__":
    app.run()
