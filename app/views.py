from app import app
from flask import  jsonify, abort, make_response, request, url_for
from flask_restful import  Api
from app.resource import *

api = Api(app, '/api/v1.0')

api.add_resource(BucketLists, '/bucketlists')
api.add_resource(BucketList, '/bucketlists/<id>')
api.add_resource(BucketListItems, '/bucketlists/<id>/items')
api.add_resource(BucketListItem, '/bucketlists/<id>/items/<item_id>')

@app.route('/')
@app.route('/index')
def index():
    return "Hello, BucketList!"

@app.route('/api/v1.0/auth/register', methods=['POST'])
def register():
	"""
	This will register a new user and returns the user credentials
	
	Endpoint: /auth/register
	Method: POST
	Parameters: username, email, password
	Response: JSON
	"""
    if not validate_data(request, ['username','email']):
        abort(400)

    user = User(request.json['username'], request.json['email'],md5(request.json.get('password', "")))
    if not save(user):
    	abort(401)

    return jsonify({'data': user.get()}), 201

@app.route('/api/v1.0/auth/login', methods=['POST'])
def login():
	"""
	This will authenticate user and provide token used to access other resources

	Endpoint: /auth/login
	Method: POST
	Parameters: username, password
	Response: JSON
	"""
    if not validate_data(request,['username','password']):
        abort(400)

    user = User.query.filter_by(username=request.json['username'],password=md5(request.json['password'])).first()
    if not user:
    	abort(403)

    return jsonify({'token': user.generate_token(),'data': user.get()}), 200

# handling errors 405
@app.errorhandler(405)
def not_found(error):
	return make_response(jsonify({'error': 'Invalid request method ' + request.method,'code':405}), 405)

# handling errors 404
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Resource not found ','code':404}), 404)

# handling errors 403
@app.errorhandler(403)
def not_found(error):
	return make_response(jsonify({'error': 'Unauthorized access','code':403}), 403)

# handling errors 400
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Bad request','code':400}), 400)

# handling errors 401
@app.errorhandler(401)
def not_found(error):
	return make_response(jsonify({'error': 'Unable to save records','code':401}), 401)
