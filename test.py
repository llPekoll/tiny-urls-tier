import os
import unittest
import tiny
from tiny import app, db


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tiny.db'
        self.app = app.test_client()
        # db.drop_all()
        # db.create_all()
        # self.populate_db() # Your function that adds test data.

    def tearDown(self):
        pass
    # def populate_db(self):
    #     pass
###############
#### tests ####
###############

    def test_01_tiny_generation(self):
        tiny_url = tiny.tiny_url_generator()
        print(len(tiny_url))

        self.assertTrue(isinstance(tiny_url, str))
        self.assertTrue(len(tiny_url) == 8)

    def test_02_url_not_in_base(self):
        response = self.app.get('jose.com')
        self.assertTrue(len(response.data) == 8)

    def test_03_tiny(self):
        response = self.app.get('/tier.app/Hk258143')
        self.assertIn(b'sdaf.com', response.data)

    def test_04_tiny_wrong(self):
        response = self.app.get('/tier.app/fsdfasdfasdfsasdf')
        self.assertIn(b"no connection", response.data)


if __name__ == "__main__":
    unittest.main()
