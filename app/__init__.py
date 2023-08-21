from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config


# create_app 함수 밖에 전역 변수로 db, migrate 객체 생성
db = SQLAlchemy()
migrate = Migrate()

# <애플리케이션 팩토리>
# create_app 함수는 플라스크 내부에서 정의된 함수 명이기 때문에,
# create_app 말고 다른 이름을 사용하면 정상 동작하지 않는다!
def create_app():
    app = Flask(__name__)
    app.config.from_object(config) # config.py 파일에 작성한 항목을 읽어오기

    # ORM 적용
    db.init_app(app)
    migrate.init_app(app, db)

    # 모델 import
    from . import models

    # 블루프린트 등록
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터 등록
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app