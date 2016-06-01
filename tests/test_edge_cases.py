import json
import unittest
from os import sys, path

from app import app, db
from app.models import *
from app.helper import *
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class TestResources(unittest.TestCase):

    """Test cases for Bucketlist Items"""

    def setUp(self):
        app.config.from_object('test_config')
        self.app = app.test_client()
        self.uid = 0
        self.token = ''
        self.bucketlist_id = 0
        self.bucketlist_item_id = 0

    def test_helper_delete_exception(self):
        bucketlist = BucketListModel('unknown', None)
        self.assertEqual(delete(bucketlist), False)

    def test_helper_get_user_id_from_token_exception(self):
        self.assertEqual(get_user_id_from_token('bucketlist'), 0)

    def test_helper_encrypt_exception(self):
        self.assertEqual(encrypt(False), False)

    def test_helper_decrypt_exception(self):
        self.assertEqual(decrypt(False), False)

    def test_model_repr(self):
        user = User('guru', '', '')
        bucketlist = BucketListModel('test', user)
        bucketlist_item = BucketListItemModel('test', bucketlist)
        print user, bucketlist, bucketlist_item

    def test_view_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_not_found(self):
        response = self.app.get('/unknown')
        self.assertEqual(response.status_code, 404)

    def test_resource_no_token(self):
        response = self.app.get('/api/v1.0/bucketlists')
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
