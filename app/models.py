from app import db


# 질문 모델 생성
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

# 답변 모델 생성
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ondelete='CASCADE': 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제된다는 의미
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    # backref: 역참조 설정 -> 한 질문에는 여러 개의 답변이 달릴 수 있는데, 역참조는 이 질문에 달린 답변들을 참조할 수 있게 함
    # ex) 어떤 질문에 해당하는 객체가 "a_question"이라면, "a_question.answer_set"과 같은 코드로 해당 질문에 달린 답변들 참조 가능
    question = db.relationship('Question', backref=db.backref('answer_set'))
    # 파이썬 코드로 질문 데이터를 삭제할 때, 연결된 답변 모두를 삭제하고자 한다면 아래와 같이 db.backref 설정
    # question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

# User 모델 생성
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)