from app import db
from datetime import datetime

class BucketListModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    #items = db.relationship('BucketListItemModel', backref='bucketlist')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user = db.relationship('User', backref=db.backref('bucketlists', lazy='dynamic'))

    def __init__(self, name):
    	self.name = name

   	def __repr__():
   		return '<BucketListModel %r>' % self.name


class BucketListItemModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(255))
    done = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucket_list_model.id'))
    bucketlist = db.relationship('BucketListModel', backref=db.backref('items', lazy='dynamic'))

    def __init__(self, task):
    	self.task = task

   	def __repr__():
   		return '<BucketListItemModel %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    #bucketlists = db.relationship('bucketlistmodel', backref='user')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username