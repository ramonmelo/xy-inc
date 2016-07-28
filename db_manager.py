
import sqlite3 as sql
from datetime import datetime as dt

class EventType(object):
    ADD = 0
    REM = 1

class DBManager(object):

    def __init__(self, app):
        """Init the connection with the database"""
        self.db = sql.connect(app.config['DATABASE'])

    def close(self):
        """Close the connection with the database"""
        self.db.close()

    def create_poi(self, name, x, y):
        """Insert a new POI into the database"""
        cursor = self.db.cursor()

        cursor.execute('INSERT INTO poi (name, x, y) VALUES (:name, :x, :y)', {
            'name': name,
            'x': x,
            'y': y
        })

        self.db.commit()

    def list_poi(self, x = None, y = None, distance = None):
        """List all POI within the range"""
        cursor = self.db.cursor()

        rows = cursor.execute('SELECT id, name, x, y FROM poi')

        for row in rows:
            pass
