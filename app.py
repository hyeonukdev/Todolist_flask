from flask import Flask
from views import main_views

UPLOAD_DIR = "images/"


def create_app():
    app = Flask(__name__)
    app.secret_key = 'sample_secret'
    app.config['UPLOAD_DIR'] = UPLOAD_DIR

    app.register_blueprint(main_views.bp)
    return app
