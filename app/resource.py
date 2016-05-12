from flask_restful import reqparse, abort, Resource
from app.models import *
from app.helper import *


parser = reqparse.RequestParser()
parser.add_argument('task')


class BucketList(Resource):
    def get(self, id):
        return {'id':id}

    def delete(self, id):
        return '', 204

    def put(self, id):
        #args = parser.parse_args()
        #task = {'task': args['task']}
        return {}, 201


class BucketLists(Resource):
    def get(self):
        bucketlists = BucketListModel.query.all()
        return [bucketlist.get() for bucketlist in bucketlists]

    def post(self):
        #args = parser.parse_args()
        #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        return {}, 201


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

