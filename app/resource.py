from flask_restful import reqparse, abort, Resource
from flask_httpauth import HTTPBasicAuth
from flask import request, make_response, jsonify
from app.models import *
from app.helper import *

auth = HTTPBasicAuth()
parser = reqparse.RequestParser()

parser.add_argument('task')

@auth.verify_password
def verify_token(username, password):
    """
    This method will verify the token and allow access to any resource that requires authentication
    """
    global token
    token = request.headers.get('AccessToken','')
    if not token:
        return False

    return decrypt(token)


@auth.error_handler
def unauthorized():
    """
    This will return a JSON error 403 response when token validation fails
    """
    return make_response(jsonify({'error': 'Unauthorized access','code':403}), 403)

class BucketList(Resource):
    @auth.login_required
    def get(self, id):
        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(403, message="Unauthorized access")

        return {'data':bucketlist.get()}

    @auth.login_required
    def delete(self, id):
        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(403, message="Unauthorized access")

        if not delete(bucketlist):
            abort(401, message="Unable to delete record")

        return {}, 204

    @auth.login_required
    def put(self, id):
        if not validate_required_fields(request, ['name']):
            abort(400, message="Missing required parameter")

        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(403, message="Unauthorized access")

        bucketlist.name = request.json['name']

        if not save(bucketlist):
            abort(409, message="Item already exists")

        return {'data':bucketlist.get()}, 201


class BucketLists(Resource):

    @auth.login_required
    def get(self):
        """
        This endpoint returns list of bucketlists based on access token.
        Method: GET
        Parameters:
            limit (optional)    default=25
            page  (optional)    default=1
        Header:   
            AccessToken  (required)

        Response: JSON
        """
        limit = int(request.args.get('limit',25))
        page = int(request.args.get('page',1))
        offset = (page * limit) - limit
        user_id = get_user_id_from_token(token)
        next_page = page + 1
        prev_page = page - 1 if page > 1 else 1
        all_list = BucketListModel.query.filter_by(created_by=int(user_id)).all()
        bucketlists = all_list[offset:(limit + offset)]
        result = {'data':[bucketlist.get() for bucketlist in bucketlists],'page':{}}
        if (limit + offset) < len(all_list):
            result['page']['next'] = "/api/v1.0/bucketlists?limit=" + str(limit) + "&page=" + str(next_page)
        
        if offset:
            result['page']['prev'] = "/api/v1.0/bucketlists?limit=" + str(limit) + "&page=" + str(prev_page)

        return result 

    @auth.login_required
    def post(self):
        """
        This endpoint returns created bucketlist details.
        Method: POST
        Parameters:
            name (required) 
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        if not validate_required_fields(request, ['name']):
            abort(400, message="Missing required parameter")

        user_id = get_user_id_from_token(token)
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(403, message="Unauthorized access")

        bucketlist = BucketListModel(request.json['name'], user)
        if not save(bucketlist):
            abort(409, message="Item already exists")

        return {'data': bucketlist.get()}, 201


class BucketListItem(Resource):
    def get(self, id, item_id):
        return {'bucketlist_id':id, 'item_id':item_id}

    def delete(self, id, item_id):
        return '', 204

    def put(self, id, item_id):
        #args = parser.parse_args()
        #task = {'task': args['task']}
        return {}, 201


class BucketListItems(Resource):
    def get(self, id):
        return []

    def post(self, id):
        #args = parser.parse_args()
        #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        return {}, 201



class Login(Resource):
    def post(self):
        """
        This will authenticate user and provide token used to access other resources

        Method: POST
        Parameters: 
            username    (required)
            password    (required)
        Response: JSON
        """

        if not validate_required_fields(request,['username','password']):
            abort(400)

        user = User.query.filter_by(username=request.json['username'],password=md5(request.json['password'])).first()

        if not user:
            abort(403)

        return {'token': user.generate_token(),'data': user.get()}, 200


class Register(Resource):

    def post(self):
        """
        This will register a new user and returns the user credentials
        
        Method: POST
        Parameters: 
            username    (required)
            email       (required)
            password    (optional) default=''

        Response: JSON
        """

        if not validate_required_fields(request, ['username','email']):
            abort(400)

        user = User(request.json['username'], request.json['email'],md5(request.json.get('password', "")))
        if not save(user):
            abort(401)

        return {'data': user.get()}, 201




