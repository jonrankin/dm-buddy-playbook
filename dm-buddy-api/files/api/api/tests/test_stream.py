# api/tests/test_stream.py

import unittest

from api import db
from api.db_access.models import User, Stream
from api.tests.base import BaseTestCase

from test_auth import register_user, login_user

import json
import time

def create_stream(self, resp_login, stream_name, stream_desc=""):
    return self.client.post(
        '/stream',
        headers=dict(
            Authorization='Bearer ' + json.loads(
                resp_login.data.decode()
            )['auth_token']
        ),
        data=json.dumps(dict(
            stream_name=stream_name,
            stream_desc=stream_desc
        )),
        content_type='application/json',
    )


class TestStreamBlueprint(BaseTestCase):

  def test_stream_create(self):
        # user registration
        resp_register = register_user(self, 'yuanti', 'yuanti@gmail.com', 'freewifi')
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['auth_token'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user(self, 'yuanti@gmail.com', 'freewifi')
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['auth_token'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)


  def test_stream_list(self):
       """ Test that we can pull all streams associated to user """

       with self.client:
        # user registration
        resp_register = register_user(self, 'yuanti', 'yuanti@gmail.com', 'freewifi')
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['auth_token'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user(self, 'yuanti@gmail.com', 'freewifi')
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['auth_token'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        #create stream
        resp_stream = create_stream(self, resp_login, 'World of Adventures', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_login['status'] == 'success')


if __name__ == '__main__':
      unittest.main()
