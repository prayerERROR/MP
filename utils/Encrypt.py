import hashlib
from MP.settings import SECRET_KEY


def md5(original_string):
    encrypter = hashlib.md5(SECRET_KEY.encode('utf-8'))
    encrypter.update(original_string.encode('utf-8'))
    return encrypter.hexdigest()

print(md5('12345678'))