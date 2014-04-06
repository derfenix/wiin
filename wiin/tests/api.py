import unittest
from wiin.init import db
from wiin.models import Users
from wiin.tests.helpers import Client


class TestApi(unittest.TestCase):
    items = []

    def setUp(self):
        self.client = Client()

    def test_login(self):
        pass

    def test_users(self):
        user = Users(1, u'test', u'test@test', '1234')
        self.items.append(user)
        db.session.add(user)
        db.session.commit()

        self.client.request('http://test.fx:5000/api/v1/users')
        self.assertGreaterEqual(self.client.response['num_results'], 2)
        self.client.request(
            'http://test.fx:5000/api/v1/users?'
            'q={"filters":[{"name":"email","op":"eq","val":"test@test"}]}'
        )
        self.assertGreaterEqual(self.client.response['num_results'], 1)
        self.assertEqual(self.client.response['objects'][0]['name'], 'test')

    def test_brands(self):
        pass

    def test_posts(self):
        pass

    def test_comments(self):
        pass

    def tearDown(self):
        for i in self.items:
            db.session.delete(i)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
