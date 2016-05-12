from Crypto.Cipher import AES
import hashlib
from app import db

def save(model):
	try:
		db.session.add(model)
		db.session.commit()
		return True
	except:
		return False


def validate_registeration_data(request):
	if not request.json or not 'email' in request.json or not 'username' in request.json:
		return False
	return True

def md5(string):
	return hashlib.md5(string.encode("utf")).hexdigest()

def encrypt(string):
	aes = AES.new('bucketlist', AES.MODE_CBC)
	return aes.encrypt(string)

def decrypt(string):
	aes = AES.new('bucketlist', AES.MODE_CBC)
	return aes.decrypt(ciphertext)