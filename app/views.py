from app import app
from flask import  jsonify, abort, make_response, request, url_for
from flask_restful import  Api
from app.resource import *

api = Api(app, prefix='/api/v1.0')

api.add_resource(Login, '/auth/login')
api.add_resource(Register, '/auth/register')
api.add_resource(BucketLists, '/bucketlists')
api.add_resource(BucketList, '/bucketlists/<id>')
api.add_resource(BucketListItems, '/bucketlists/<id>/items')
api.add_resource(BucketListItem, '/bucketlists/<id>/items/<item_id>')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, BucketList!"
