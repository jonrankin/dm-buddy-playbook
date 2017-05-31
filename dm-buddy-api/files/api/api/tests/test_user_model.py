import unittest

from api import db
from api.db_access.models import User
from api.tests.base import BaseTestCase

class TestUserModel(BaseTestCase):

    def test_user_creation(self):
        user = User(
            username='testUser2',
            email='test2@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        verify_user = User.query.filter_by(email='test2@test.com').first()

    def test_encode_auth_token(self):
        user = User(
            username='testUser',
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            username='testUser',
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8") ) == 1)


if __name__ == '__main__':
    unittest.main()
