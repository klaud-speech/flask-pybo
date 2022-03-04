from flask import Blueprint, url_for
from werkzeug.utils import redirect

# 동일한 URl 페이지로 묶어준다.
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/test')
def test_pybo():
    return 'Pybo, Python(+Flask) 테스트 페이지입니다.'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))


