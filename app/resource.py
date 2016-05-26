from flask_restful import reqparse, abort, Resource
from flask_httpauth import HTTPBasicAuth
from flask import request, make_response, jsonify
from app.models import *
from app.helper import *

auth = HTTPBasicAuth()

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
        """
        This endpoint returns bucketlists details of a given bucketlist id.
        Method: GET
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(404, message="Bucketlist not found")

        return bucketlist.get()

    @auth.login_required
    def delete(self, id):
        """
        This endpoint deletes a given bucketlist id from the database.
        Method: DELETE
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(404, message="Bucketlist not found")

        if len(bucketlist.items.all()):
            abort(400, message="This Item is associated with bucketlist items")

        if not delete(bucketlist):
            abort(401, message="Unable to delete record")

        return {}, 204

    @auth.login_required
    def put(self, id):
        """
        This endpoint returns updated bucketlist details of a given bucketlist id.
        Method: PUT
        Parameters:
            name (required) 
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        args = validate_args({'name':True})
        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(404, message="Bucketlist not found")

        bucketlist.name = args['name']

        if not save(bucketlist):
            abort(409, message="Item already exists")

        return bucketlist.get(), 201


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

        limit = int(request.args.get('limit',20))
        if limit > 100:
            limit = 100

        page = int(request.args.get('page',1))
        q = request.args.get('q','')
        offset = (page * limit) - limit
        user_id = get_user_id_from_token(token)
        next_page = page + 1
        prev_page = page - 1 if page > 1 else 1
        all_list = BucketListModel.query.filter(BucketListModel.name.like("%" + q + "%"), BucketListModel.created_by.is_(user_id)).all()
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

        args = validate_args({'name':True})
        user_id = get_user_id_from_token(token)
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")

        bucketlist = BucketListModel(args['name'], user)
        if not save(bucketlist):
            abort(409, message="Item already exists")

        return bucketlist.get(), 201


class BucketListItem(Resource):

    @auth.login_required
    def get(self, id, item_id):
        """
        This endpoint returns bucketlists item details of a given bucketlist item id.
        Method: GET
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(404, message="Bucketlist not found")
            
        item = BucketListItemModel.query.filter_by(bucketlist_id=bucketlist.id, id=int(item_id)).first()
        if not item:
            abort(400, message="Bucketlist Item does not exist")

        return item.get(), 200

    @auth.login_required
    def put(self, id, item_id):
        """
        This endpoint returns updated bucketlist item details of a given bucketlist item id.
        Method: PUT
        Parameters:
            task (optional) 
            done (optional) 
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        args = validate_args({'task':False,'done':False})
        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(404, message="Bucketlist not found")
            
        item = BucketListItemModel.query.filter_by(bucketlist_id=bucketlist.id, id=int(item_id)).first()
        if not item:
            abort(400, message="Bucketlist Item does not exist")

        if args.get('task'):
            item.task = args.get('task')
         
        if args.get('done'):
            item.done = True if args.get('done') == 'true' else False
            
        if not save(item):
            abort(409, message="Unable to update record")

        return item.get(), 201


class BucketListItems(Resource):
    
    @auth.login_required
    def get(self, id):
        """
        This endpoint returns list of bucketlist items based on access token and bucketlist id.
        Method: GET
        Parameters:
            limit (optional)    default=25
            page  (optional)    default=1
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(403, message="Unauthorized access")

        limit = int(request.args.get('limit',20))
        if limit > 100:
            limit = 100
            
        page = int(request.args.get('page',1))
        q = request.args.get('q','')
        offset = (page * limit) - limit
        user_id = get_user_id_from_token(token)
        next_page = page + 1
        prev_page = page - 1 if page > 1 else 1
        all_items = BucketListItemModel.query.filter(
            BucketListItemModel.task.like("%" + q + "%"), 
            BucketListItemModel.bucketlist_id.is_(bucketlist.id)
            ).all()
        items = all_items[offset:(limit + offset)]
        result = {'data':[item.get() for item in items],'page':{}}
        if (limit + offset) < len(all_items):
            result['page']['next'] = "/api/v1.0/bucketlists/" + str(id) + "?limit=" + str(limit) + "&page=" + str(next_page)
        
        if offset:
            result['page']['prev'] = "/api/v1.0/bucketlists" + str(id) + "?limit=" + str(limit) + "&page=" + str(prev_page)

        return result

    @auth.login_required
    def post(self, id):
        """
        This endpoint returns created bucketlist item details.
        Method: POST
        Parameters:
            task (required) 
        Header:   
            AccessToken  (required)

        Response: JSON
        """

        args = validate_args({'task':True})
        user_id = get_user_id_from_token(token)
        bucketlist = BucketListModel.query.filter_by(id=id, created_by=int(user_id)).first()
        if not bucketlist:
            abort(404, message="Bucketlist not found")
        
        item = BucketListItemModel(args['task'], bucketlist)    
        if not save(item):
            abort(409, message="Item already exists")

        return item.get(), 201



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
        
        args = validate_args({'username':True, 'password':True})
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            abort(403, message='Invalid username')

        if user.password != md5(args['password']):
            abort(403, message="Incorrect password")

        return {'token': user.generate_token()}, 200


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

        args = validate_args({'username':True, 'password':True, 'email':True})
        user = User(args['username'], args['email'], md5(args['password']))
        if not save(user):
            abort(401, message="User already exists")

        return user.get(), 201




