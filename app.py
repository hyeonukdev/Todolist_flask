import os
from flask import Flask
from views import main_views

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(ROOT_DIR, 'images')

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super_secret_key'
    app.config['UPLOAD_DIR'] = UPLOAD_DIR

    app.register_blueprint(main_views.bp)
    return app
