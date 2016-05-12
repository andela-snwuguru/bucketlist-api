from itsdangerous import TimestampSigner
import hashlib
from app import db

encrypt_key = 'bucketlists api'

def save(model):
	try:
		db.session.add(model)
		db.session.commit()
		return True
	except:
		return False


def validate_data(request, required=[]):
	if not request.json:
		return False

	for field in required:
		if not field in request.json:
			return False
	return True

def md5(string):
	return hashlib.md5(string.encode("utf")).hexdigest()

def encrypt(string):
	signer = TimestampSigner(encrypt_key)
	return signer.sign(string)

def decrypt(string, max_age=5):
	try:
		signer = TimestampSigner(encrypt_key)
		return signer.unsign(string, max_age=max_age)
	except:
		return False
