from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app import db
from app.forms import UserCreateForm, UserLoginForm
from app.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data), # 비밀번호는 암호화하여 저장
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        # 해당 사용자가 존재하는지 확인
        if not user:
            error = '존재하지 않는 사용자입니다.'
        # 사용자가 존재한다면 입력 받은 비밀번호가 데이터베이스 내의 비밀번호와 일치하는지 확인
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 올바르지 않습니다.'
        # 사용자도 존재하고 비밀번호도 일치하는 경우, 세션에 사용자 정보를 저장
        # >> session은 request와 마찬가지로 플라스크가 자체적으로 생성하여 제공하는 객체
        # >> 브라우저가 flask 서버에 요청을 보내면, request 객체는 요청할 때마다 새로운 객체가 생성
        # >> 반면, session은 request와 달리 한번 생성하면 그 값을 계속 유지
        # >> 즉, 세션은 서버에 브라우저 별로 생성되는 메모리 공간이다!
        # >> 다시 말해, 세션에 사용자의 id 값을 저장하면 다양한 URL 요청에 이 세션에 저장된 값을 읽을 수 있다!
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

# 아래와 같이 애너테이션이 적용된 함수는 라우팅 함수보다 항상 먼저 실행된다!
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))