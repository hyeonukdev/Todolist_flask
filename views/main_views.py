from flask import Blueprint


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    return 'index'


@bp.route('/test')
def test():
    return 'test'