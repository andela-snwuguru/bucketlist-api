from app import app
from flask import  jsonify, abort, make_response, request, url_for
from flask_restful import  Api
from app.resource import *

api = Api(app)

api.add_resource(BucketLists, '/api/v1.0/bucketlists')
api.add_resource(BucketList, '/api/v1.0/bucketlists/<id>')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, BucketList!"
