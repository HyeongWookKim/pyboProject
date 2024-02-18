import os

BASE_DIR = os.path.dirname(__file__)

# 데이터베이스 접속 주소 설정
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "pybo.db")}'
# SQLAlchemy의 이벤트를 처리하는 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False # 옵션 비활성화
# CSRF(Cross-Site Request Forgery) 토큰 생성을 위한 비밀키 설정
SECRET_KEY = 'dev'