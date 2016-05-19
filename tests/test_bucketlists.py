import unittest
import json
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app import app, db
from app.models import *
from app.helper import delete


class TestResources(unittest.TestCase):
	"""Test cases for Resources"""

	def register(self):
		if self.uid:
			return

		user = {'username':'tuser', 'password':'test','email':'tuser@mail.com'}
		response = self.app.post('/api/v1.0/auth/register',data=user)
		self.assertEqual(response.status_code, 201)
		result = json.loads(response.data)
		if not result.get('message'):
			self.uid = result['data']['id']
        	self.token = self.get_token()
   

   	def tearDown(self):
   		""" Clean up database """
   		self.remove_user()
   		self.remove_bucketlist()

	def get_token(self):
		""" Login to retrieve access token """

		user = {'username':'tuser', 'password':'test'}
		response = self.app.post('/api/v1.0/auth/login',data=user)
		result = json.loads(response.data)
		return result.get('token','')

	def setUp(self):
		app.config.from_object('test_config')
		self.app = app.test_client()
		self.uid = 0
		self.token = ''
		self.bucketlist_id = 0
		self.bucketlist_item_id = 0


	def remove_user(self):
		""" Remove user record """

		user = User.query.filter_by(id=self.uid).first()
		if user:
			delete(user)
        
	def remove_bucketlist(self):
		""" Remove bucketlist record """

		bucketlist = BucketListModel.query.filter_by(id=self.bucketlist_id).first()
		if bucketlist:
			delete(bucketlist)
        
        
	def new_bucketlist(self):
		""" Post to bucketlists endpoint """

		new_bucketlists = self.app.post('/api/v1.0/bucketlists', data={'name':'test item 1'}, 
			headers={'AccessToken':self.token})
		self.assertEqual(new_bucketlists.status_code, 201)
		new_bucketlists_result = json.loads(new_bucketlists.data)
		if new_bucketlists_result.get('data'):
			self.bucketlist_id = new_bucketlists_result['data']['id']
		duplicate_bucketlists = self.app.post('/api/v1.0/bucketlists',data={'name':'test item 1'} , 
			headers={'AccessToken':self.token})
		self.assertEqual(duplicate_bucketlists.status_code, 409)
       
	def new_bucketlist_item(self):
		# posting to bucketlists endpoint
		new_bucketlist_item = self.app.post('/api/v1.0/bucketlists/' + str(self.bucketlist_id) + '/items', 
			data={'task':'buy a private jet'}, 
			headers={'AccessToken':self.token})

		self.assertEqual(new_bucketlist_item.status_code, 201)
		new_bucketlist_item_result = json.loads(new_bucketlist_item.data)
		self.assertNotEqual(new_bucketlist_item_result.get('data'), None)

	def get_bucketlists(self):
		""" Get bucketlists """

		get_bucketlists = self.app.get('/api/v1.0/bucketlists', headers={'AccessToken':self.token})
		self.assertEqual(get_bucketlists.status_code, 200)
		get_result = json.loads(get_bucketlists.data)
		self.assertNotEqual(get_result.get('data'), None)

	def get_single_bucketlist(self):
		""" Get bucketlists single item """

		get_bucketlists = self.app.get('/api/v1.0/bucketlists/'+ str(self.bucketlist_id), 
			headers={'AccessToken':self.token})
		self.assertEqual(get_bucketlists.status_code, 200)
		get_result = json.loads(get_bucketlists.data)
		self.assertNotEqual(get_result.get('data'), None)

	def update_bucketist(self):
		""" Update bucketlists """

		put_bucketlists = self.app.put('/api/v1.0/bucketlists/'+ str(self.bucketlist_id), 
			data={'name':'test item modified'}, headers={'AccessToken':self.token})
		self.assertEqual(put_bucketlists.status_code, 201)
		put_result = json.loads(put_bucketlists.data)
		data = put_result.get('data')
		self.assertEqual(str(data['name']), 'test item modified')

	def delete_bucketlist(self):
		""" Delete bucketlists """

		del_bucketlists = self.app.delete('/api/v1.0/bucketlists/'+ str(self.bucketlist_id), 
			headers={'AccessToken':self.token})
		self.assertEqual(del_bucketlists.status_code, 204)

	def test_bucketlists_endpoint(self):
		""" Test all endpoints of bucketlists """

		self.register()
		self.new_bucketlist()
		self.get_bucketlists()
		self.get_single_bucketlist()
		self.update_bucketist()
		self.delete_bucketlist()
		

if __name__ == '__main__':
	unittest.main()