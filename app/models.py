from app import db

class BucketListModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self):
    	print 'here'
