from datetime import datetime
from app import db
from app.helper import encrypt, decrypt


class BucketListModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    user = db.relationship(
        'User', backref=db.backref('bucketlists', lazy='dynamic'))

    def __init__(self, name, user):
        self.name = name
        self.user = user

    def get(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_by': self.user.username,
            'date_created': str(self.date_created),
            'date_modified': str(self.date_modified),
            'items': self.get_items()
        }

    def get_items(self):
        items = self.items.all()
        data = []
        for item in items:
            data.append(item.get())
        return data

    def __repr__(self):
        return '<BucketListModel %r>' % self.name


class BucketListItemModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(255))
    done = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey('bucket_list_model.id'))
    bucketlist = db.relationship(
        'BucketListModel', backref=db.backref('items', lazy='dynamic'))

    def __init__(self, task, bucketlist):
        self.task = task
        self.bucketlist = bucketlist

    def get(self):
        return {
            'id': self.id,
            'task': self.task,
            'done': self.done,
            'bucketlists': self.bucketlist.name,
            'date_created': str(self.date_created),
            'date_modified': str(self.date_modified)
        }

    def __repr__(self):
        return '<BucketListItemModel %r>' % self.task


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(200), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def get(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': str(self.date_created),
            'date_modified': str(self.date_modified),
        }

    def generate_token(self):
        string = str(self.password) + '|' + str(self.id) + '|'
        return encrypt(string)
