# utils.py
from hashids import Hashids


def create_hashid(id):
    hashids = Hashids(min_length=5, salt=current_app.config['super_secret_key'])
    hashid = hashids.encode(id)
    return hashid


def decode_hashid(hashid):
    hashids = Hashids(min_length=5, salt=current_app.config['super_secret_key'])
    id = hashids.decode(hashid)
    return id
