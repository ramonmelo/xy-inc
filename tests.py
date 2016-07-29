
import os
import unittest
import tempfile

import server # App Module

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

        with server.app.app_context():
            server.db.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
