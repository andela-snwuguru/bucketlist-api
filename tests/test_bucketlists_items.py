import unittest
import json
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app import app, db
from app.models import *
from app.helper import delete


class TestBucketlistItemResources(unittest.TestCase):
	"""Test cases for Bucketlist Items"""

	def register(self):
		""" Register new user """
		if self.uid:
			return

		user = {'username':'tuser', 'password':'test','email':'tuser@mail.com'}
		response = self.app.post('/api/v1.0/auth/register',data=user)
		self.assertEqual(response.status_code, 201)

		duplicate_response = self.app.post('/api/v1.0/auth/register',data=user)
		self.assertEqual(duplicate_response.status_code, 401)

		result = json.loads(response.data)
		if not result.get('message'):
			self.uid = result['data']['id']
        	self.token = self.get_token()
   

   	def tearDown(self):
   		""" Clean up the database """

   		self.remove_user()
   		self.remove_bucketlist()
   		self.remove_bucketlist_item()

	def get_token(self):
		""" Login to retrieve access token """

		user = {'username':'tuserfake', 'password':'test'}
		response = self.app.post('/api/v1.0/auth/login',data=user)
		self.assertEqual(response.status_code, 403)

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
            
	def remove_bucketlist_item(self):
		""" Remove bucketlist item """

		item = BucketListItemModel.query.filter_by(id=self.bucketlist_item_id).first()
		if item:
			delete(item)
        
        
	def new_bucketlist(self):
		""" Posting to bucketlists endpoint """

		new_bucketlists = self.app.post('/api/v1.0/bucketlists', data={'name':'test item 1'}, 
			headers={'AccessToken':self.token})
		self.assertEqual(new_bucketlists.status_code, 201)
		new_bucketlists_result = json.loads(new_bucketlists.data)
		if new_bucketlists_result.get('data'):
			self.bucketlist_id = new_bucketlists_result['data']['id']
		
       
	def new_bucketlist_item(self):
		""" Posting to bucketlists endpoint """

		new_bucketlist_item = self.app.post('/api/v1.0/bucketlists/0' + '/items', 
			data={'task':'buy a private jet'}, 
			headers={'AccessToken':self.token})
		self.assertEqual(new_bucketlist_item.status_code, 403)
		
		new_bucketlist_item = self.app.post('/api/v1.0/bucketlists/' + str(self.bucketlist_id) + '/items', 
			data={'task':'buy a private jet'}, 
			headers={'AccessToken':self.token})
		self.assertEqual(new_bucketlist_item.status_code, 201)

		new_bucketlist_item_result = json.loads(new_bucketlist_item.data)
		self.assertNotEqual(new_bucketlist_item_result.get('data'), None)
		if new_bucketlist_item_result:
			self.bucketlist_item_id = new_bucketlist_item_result['data']['id']

	def get_items(self):
		""" Get bucketlist Items """
		get_items = self.app.get('/api/v1.0/bucketlists/'  + str(self.bucketlist_id) + '/items', 
			headers={'AccessToken':self.token})
		self.assertEqual(get_items.status_code, 200)
		get_result = json.loads(get_items.data)
		self.assertNotEqual(get_result.get('data'), None)


	def get_single_item(self):
		""" Get bucketlist Item """

		get_item = self.app.get('/api/v1.0/bucketlists/'  + str(self.bucketlist_id) + '/items/' + str(self.bucketlist_item_id), 
			headers={'AccessToken':self.token})
		self.assertEqual(get_item.status_code, 200)
		get_result = json.loads(get_item.data)
		self.assertNotEqual(get_result.get('data'), None)

	def update_item(self):
		""" Update bucketlist item """

		put_item = self.app.put('/api/v1.0/bucketlists/0' + '/items/' + str(self.bucketlist_item_id), 
			data={'done':True}, headers={'AccessToken':self.token})
		self.assertEqual(put_item.status_code, 403)

		put_item = self.app.put('/api/v1.0/bucketlists/'  + str(self.bucketlist_id) + '/items/' + str(self.bucketlist_item_id), 
			data={'done':True}, headers={'AccessToken':self.token})
		self.assertEqual(put_item.status_code, 201)
		put_result = json.loads(put_item.data)
		data = put_result.get('data')
		self.assertEqual(data['done'], True)


	def delete_bucketlist(self):
		""" Delete bucketlists """

		del_bucketlists = self.app.delete('/api/v1.0/bucketlists/'+ str(self.bucketlist_id), 
			headers={'AccessToken':self.token})
		self.assertEqual(del_bucketlists.status_code, 400)

		del_bucketlists = self.app.delete('/api/v1.0/bucketlists/0', 
			headers={'AccessToken':self.token})
		self.assertEqual(del_bucketlists.status_code, 403)

	def delete_item(self):
		""" Delete bucketlist item """

		del_item = self.app.delete('/api/v1.0/bucketlists/0'+ '/items/' + str(self.bucketlist_item_id), 
			headers={'AccessToken':self.token})
		self.assertEqual(del_item.status_code, 403)

		del_item = self.app.delete('/api/v1.0/bucketlists/'+ str(self.bucketlist_id) + '/items/' + str(self.bucketlist_item_id), 
			headers={'AccessToken':self.token})
		self.assertEqual(del_item.status_code, 204)

	def test_bucketlists_endpoint(self):
		""" Test all endpoint of bucketlist items """

		self.register()
		self.new_bucketlist()
		self.new_bucketlist_item()
		self.get_items()
		self.update_item()
		self.get_single_item()
		self.delete_bucketlist()
		self.delete_item()



if __name__ == '__main__':
	unittest.main()