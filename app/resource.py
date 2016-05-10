from flask_restful import reqparse, abort, Resource
from app.models import *


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
        return []

    def post(self):
        #args = parser.parse_args()
        #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        return {}, 201
