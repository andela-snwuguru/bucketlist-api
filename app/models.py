from app import db

class BucketListModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
    	self.name = name

   	def __repr__():
   		return '<BucketListModel %r>' % self.name


class BucketListItemModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(255))

    def __init__(self, task):
    	self.task = task

   	def __repr__():
   		return '<BucketListItemModel %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username