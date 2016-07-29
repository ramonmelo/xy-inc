
import sqlite3 as sql
from math import sqrt, pow

class DBManager(object):

    COLUMN_NAMES = ['id', 'name', 'x', 'y']

    def __init__(self, app):
        """Init the connection with the database"""
        self.app = app

    def init_db(self):
        self.db = sql.connect(self.app.config['DATABASE'])

        with open(self.app.config['DATABASE_SCHEME'], 'r') as scheme_file:

            cursor = self.db.cursor()
            cursor.execute(scheme_file.read())

            self.db.commit()

    def close(self):
        """Close the connection with the database"""
        self.db.close()

    def create_poi(self, name, x, y):
        """Insert a new POI into the database"""

        assert type(name) is str
        assert type(x) is int
        assert type(y) is int
        assert len(name) >= 1
        assert x >= 0
        assert y >= 0

        cursor = self.db.cursor()

        cursor.execute('INSERT INTO poi (name, x, y) VALUES (:name, :x, :y)', {
            'name': name,
            'x': x,
            'y': y
        })

        self.db.commit()

    def list_poi(self, x_base = None, y_base = None, distance = None):
        """List all POI within the range"""

        has_filter = False
        if (x_base is not None) and (y_base is not None) and (distance is not None):
            assert type(x_base) is int
            assert type(y_base) is int
            assert type(distance) is int

            has_filter = True

        cursor = self.db.cursor()

        result = []

        for idx, name, x, y in cursor.execute('SELECT id, name, x, y FROM poi'):

            if has_filter:
                diff = sqrt( pow(x_base - x, 2) + pow(y_base - y, 2) )

                if diff > distance:
                    continue

            result.append({
                'id': idx,
                'name': name,
                'x': x,
                'y': y
            })

        return result
