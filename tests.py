
import os
import unittest
import tempfile
from flask import json

from urllib.parse import urlencode

import server # App Module

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        self.db = server.db

        with server.app.app_context():
            server.db.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

        self.db.close()

    # Utils

    def find_poi_with(self, values = {}):
        response = self.app.get('/list_poi/?' + urlencode(values))
        data = response.get_data()

        return response, data

    def create_poi_with(self, values):
        response = self.app.post('/create_poi/', data = values)
        data = response.get_data()

        return response, data

    # Tests for create

    def test_create_poi_all_data(self):
        response, data = self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert data['msg'] == 'Saved with success.'

    def test_create_poi_missing_name(self):
        response, data = self.create_poi_with(dict(
            x = '0',
            y = '0'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert data['msg'] == 'Please, send all data values.'

    def test_create_poi_missing_x(self):
        response, data = self.create_poi_with(dict(
            name = 'poi1',
            y = '0'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert data['msg'] == 'Please, send all data values.'

    def test_create_poi_missing_y(self):
        response, data = self.create_poi_with(dict(
            name = 'poi1',
            x = '0'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert data['msg'] == 'Please, send all data values.'

    def test_create_poi_wrong_x(self):
        response, data = self.create_poi_with(dict(
            name = 'poi1',
            x = 'abc',
            y = '0'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert data['msg'] == 'Please, send valid values.'

    def test_create_poi_wrong_y(self):
        response, data = self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = 'abc'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert data['msg'] == 'Please, send valid values.'

    # Tests for database insert

    def test_db_create_ok(self):
        self.db.create_poi('poi1', 0, 0)

    def test_db_create_wrong_name(self):
        with self.assertRaises(AssertionError):
            self.db.create_poi(123, 0, 0)

    def test_db_create_wrong_x(self):
        with self.assertRaises(AssertionError):
            self.db.create_poi('poi1', 'abc', 0)

    def test_db_create_wrong_y(self):
        with self.assertRaises(AssertionError):
            self.db.create_poi('poi1', 0, 'abc')

    def test_db_create_short_name(self):
        with self.assertRaises(AssertionError):
            self.db.create_poi('', 0, 0)

    def test_db_create_negative_x(self):
        with self.assertRaises(AssertionError):
            self.db.create_poi('poi1', -1, 0)

    def test_db_create_negative_y(self):
        with self.assertRaises(AssertionError):
            self.db.create_poi('poi1', 0, -1)

    # Tests for list and filter

    def test_list_empty_db(self):
        response, data = self.find_poi_with()

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert len(data['result']) == 0

    def test_list_one_poi(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with()

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert len(data['result']) == 1

        assert data['result'][0]['name'] == 'poi1'
        assert data['result'][0]['x'] == 0
        assert data['result'][0]['y'] == 0

    def test_list_with_empty_filters(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '',
            y = '',
            distance = ''
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert len(data['result']) == 1

        assert data['result'][0]['name'] == 'poi1'
        assert data['result'][0]['x'] == 0
        assert data['result'][0]['y'] == 0

    def test_list_valid_filters(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '0',
            y = '0',
            distance = '1'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert len(data['result']) == 1

        assert data['result'][0]['name'] == 'poi1'
        assert data['result'][0]['x'] == 0
        assert data['result'][0]['y'] == 0

    def test_list_valid_filters_missing_x(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '',
            y = '0',
            distance = '1'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert len(data['result']) == 1

        assert data['result'][0]['name'] == 'poi1'
        assert data['result'][0]['x'] == 0
        assert data['result'][0]['y'] == 0

    def test_list_valid_filters_missing_y(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '0',
            y = '',
            distance = '1'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert len(data['result']) == 1

        assert data['result'][0]['name'] == 'poi1'
        assert data['result'][0]['x'] == 0
        assert data['result'][0]['y'] == 0

    def test_list_valid_filters_missing_distance(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '0',
            y = '0',
            distance = ''
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert len(data['result']) == 1

        assert data['result'][0]['name'] == 'poi1'
        assert data['result'][0]['x'] == 0
        assert data['result'][0]['y'] == 0

    def test_list_wrong_x(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = 'abc',
            y = '0',
            distance = '0'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert len(data['result']) == 0
        assert data['msg'] == 'Please, send valid values.'

    def test_list_wrong_y(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '0',
            y = 'abc',
            distance = '0'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert len(data['result']) == 0
        assert data['msg'] == 'Please, send valid values.'

    def test_list_wrong_distance(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '0',
            y = '0',
            distance = 'abc'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert len(data['result']) == 0
        assert data['msg'] == 'Please, send valid values.'

    def test_list_away_from_range(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        response, data = self.find_poi_with(dict(
            x = '5',
            y = '5',
            distance = '1'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is True
        assert len(data['result']) == 0
        assert data['msg'] == 'No results were found with current filters.'

    def test_list_within_range(self):
        self.create_poi_with(dict(
            name = 'poi1',
            x = '0',
            y = '0'
        ))

        self.create_poi_with(dict(
            name = 'poi2',
            x = '4',
            y = '4'
        ))

        self.create_poi_with(dict(
            name = 'poi3',
            x = '7',
            y = '7'
        ))

        response, data = self.find_poi_with(dict(
            x = '5',
            y = '5',
            distance = '2'
        ))

        assert response.status_code is 200
        assert len(data) != 0

        data = json.loads(data)

        assert data['error'] is False
        assert len(data['result']) == 1

        assert data['result'][0]['name'] == 'poi2'
        assert data['result'][0]['x'] == 4
        assert data['result'][0]['y'] == 4


if __name__ == '__main__':
    unittest.main()
