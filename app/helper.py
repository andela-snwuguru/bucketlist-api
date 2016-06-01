from flask_restful import reqparse
import hashlib
from itsdangerous import TimestampSigner
from app import db

encrypt_key = 'bucketlists api'


def save(model):
    """ Save a row in the database """
    try:
        db.session.add(model)
        db.session.commit()
        return True
    except:
        return False


def delete(model):
    """ Deletes a row from the database """
    try:
        db.session.delete(model)
        db.session.commit()
        return True
    except:
        return False


def get_user_id_from_token(token):
    """
    This method extracts the user id from provided access token
    """
    data = token.split('|')
    try:
        return data[1]
    except:
        return 0


def validate_args(fields={}):
    """
    This method helps to parse and validate provided parameters.
    It will return parsed argument if the require fields are in request
    """
    parser = reqparse.RequestParser()
    for field in fields.keys():
        help_message = field + ' can not be blank'
        parser.add_argument(field, required=fields[field], help=help_message)

    return parser.parse_args()


def md5(string):
    """
    This method will return md5 hash of a given string
    """
    return hashlib.md5(string.encode("utf")).hexdigest()


def encrypt(string):
    """
    This method will return encrypted version of a string.
    It will return False if encryption fails
    """
    try:
        signer = TimestampSigner(encrypt_key)
        return signer.sign(string)
    except:
        return False


def decrypt(string, max_age=15000):
    """
    This method will return decrypted version of an encrypted string.
    If age of encryption is greater than max age it will return False
    """
    try:
        signer = TimestampSigner(encrypt_key)
        return signer.unsign(string, max_age=max_age)
    except:
        return False
