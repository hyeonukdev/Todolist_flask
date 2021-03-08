import os
from flask import Flask
from views import main_views
from logging.config import dictConfig
# from flask_restplus import Resource, Api

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(ROOT_DIR, 'images/')


def create_app():
    app = Flask(__name__)
    app.secret_key = 'super_secret_key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

    # api = Api(
    #     app,
    #     version='0.1',
    #     title="Todo's API Server",
    #     description="Todo's API Server!",
    #     terms_url="/api/",
    #     contact="khu@xinapse.com",
    #     license="MIT"
    # )
    #
    # ns = api.namespace('custom', description='operations')
    #
    # app.config.SWAGGER_UI_DOC_EXPANSION = 'full'


    app.register_blueprint(main_views.bp)
    return app


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/error.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})


