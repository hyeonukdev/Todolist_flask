# from flask import Flask
# from flask.ext.bcrypt import Bcrypt
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'I am your father'
app.config['BCRYPT_LEVEL'] = 10

bcrypt = Bcrypt(app)

pw_hash = bcrypt.generate_password_hash('password')
pw_hash2 = bcrypt.generate_password_hash('password')

bcrypt.check_password_hash(pw_hash, 'password') # True
pw_hash == pw_hash2 # False