from flask import Blueprint, url_for
from werkzeug.utils import redirect


# 블루프린트 생성
bp = Blueprint('main', __name__, url_prefix='/') # 'main'은 블루프린트의 별칭

# 블루프린트에 라우팅 함수 추가
@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    # redirect(URL): URL로 페이지를 이동
    # url_for(라우팅 함수명): 라우팅 함수에 매핑되어 있는 URL을 리턴
    return redirect(url_for('question._list'))