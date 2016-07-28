
import sqlite3 as sql
from math import sqrt

class DBManager(object):

    COLUMN_NAMES = ['id', 'name', 'x', 'y']

    def __init__(self, app):
        """Init the connection with the database"""
        self.db = sql.connect(app.config['DATABASE'])

    def close(self):
        """Close the connection with the database"""
        self.db.close()

    def create_poi(self, name, x, y):
        """Insert a new POI into the database"""

        assert type(name) is str
        assert type(x) is int
        assert type(y) is int

        cursor = self.db.cursor()

        cursor.execute('INSERT INTO poi (name, x, y) VALUES (:name, :x, :y)', {
            'name': name,
            'x': x,
            'y': y
        })

        self.db.commit()

    # def get_poi(self, name):
    #     """Return a single POI by its name"""
    #     cursor = self.db.cursor()

    #     result = cursor.execute('SELECT :columns FROM poi WHERE name = :name', {
    #         'columns': COLUMN_NAMES.join(','),
    #         'name': name
    #     })
    #     row = result.fetchone()

    #     # if row:
    #         # return row

    #     return row

    def list_poi(self, x = None, y = None, distance = None):
        """List all POI within the range"""

        # has_filter = False

        sql = 'SELECT id, name, x, y FROM poi'

        # if x or y or distance:
        #     assert type(x) is int
        #     assert type(y) is int
        #     assert type(distance) is int

        #     has_filter = True

        cursor = self.db.cursor()

        result = []

        for idx, name, x, y in cursor.execute(sql):
            result.append({
                'id': idx,
                'name': name,
                'x': x,
                'y': y
            })

        return result
