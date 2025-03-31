# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

from app import db

class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    qualification = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(20),nullable=False)

class Subjects(db.Model):
    __tablename__ = "subjects"
    subject_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

class Chapter(db.Model):
    __tablename__ = "chapter"
    chapter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_name= db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.subject_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

class Question(db.Model):
    __tablename__ = "question"
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_title = db.Column(db.String(50), nullable=False)
    question_statement = db.Column(db.String(50), nullable=False)
    quiz_id = db.Column(db.String(50), nullable=False)
    option1 = db.Column(db.String(50), nullable=False)
    option2 = db.Column(db.String(50), nullable=False)
    option3 = db.Column(db.String(50), nullable=False)
    option4 = db.Column(db.String(50), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    no_question = db.Column(db.Integer, nullable=False)
    
class Quiz(db.Model):
    __tablename__ = "quiz"
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.chapter_id"), nullable=False)
    marks=db.Column(db.Integer,nullable=False)
    quiz_name=db.Column(db.String(50),nullable=False)

class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.subject_id"), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.chapter_id"), nullable=False)
    quizID = db.Column(db.String(100), nullable=False)


class ScoreView(db.Model):
    __tablename__ = "score_view"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Text, nullable=False)
    user_name = db.Column(db.String(255), nullable=False)  # Assuming email as username
    subject_name = db.Column(db.String(255), nullable=False)
    chapter_name = db.Column(db.String(255), nullable=False)
    quiz_name = db.Column(db.String(255), nullable=True)  # Quiz name can be NULL

    def __repr__(self):
        return f"<ScoreView(id={self.id}, score={self.score}, user_name='{self.user_name}', subject_name='{self.subject_name}', chapter_name='{self.chapter_name}', quiz_name='{self.quiz_name}')>"