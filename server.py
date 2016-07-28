
import os
import sqlite3
from flask import Flask

from db_manager import DBManager

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'db.sqlite')
))

db = DBManager(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/create")
def create_poi():
    pass

@app.route("/list")
def list_poi():
    pass

if __name__ == "__main__":
    app.run()
