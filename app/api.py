from .models import Users, Subjects, Chapter,Question,Quiz,Score
from app import db
from flask_restful import Resource, reqparse
from datetime import datetime, timezone

# 1. Users Table
Users_parser = reqparse.RequestParser()
Users_parser.add_argument('email', type=str, required=True, help='Email is required')
Users_parser.add_argument('password', type=str, required=True, help='Password is required')
Users_parser.add_argument('qualification', type=str, required=True, help='qualification is required')
Users_parser.add_argument('role', type=str, required=False, help='role is required')
Users_parser.add_argument('dob', type=int, required=False, help='dob is optional')

# 2.Chapter Table
chapter_parser=reqparse.RequestParser()
chapter_parser.add_argument('description',type=str,required=True,help="description is required")
chapter_parser.add_argument('subject_id',type=int,required=True,help='subject_id is required')
chapter_parser.add_argument('user_id',type=int,required=True,help='user_id is required')
chapter_parser.add_argument('chapter_name',type=str,required=True,help="dchapter_name is required")

# 3.Quiz Table

Quiz_parser = reqparse.RequestParser()
Quiz_parser.add_argument('date',type=str,required=True, help= 'data is required')
Quiz_parser.add_argument('duration', type=int,required=True,help='duration is required')
Quiz_parser.add_argument('chapter_id', type= int,required=True,help='chapter_id is required')
Quiz_parser.add_argument('marks', type= int,required=True,help='total marks is required')
Quiz_parser.add_argument('quiz_name', type= str,required=True,help='quiz_name is required')

# 4.Subject Table

Subjects_parser = reqparse.RequestParser()
Subjects_parser.add_argument('subject_name',type=str, required= True, help= 'subject_name is required')
Subjects_parser.add_argument('description',type=str, required= True, help= 'description is required')
Subjects_parser.add_argument('user_id',type=int, required= True, help= 'user_id is required')

# 5.Questions Table

Question_parser= reqparse.RequestParser()
Question_parser.add_argument('question_title',type=str,required=True,help='question title is required')
Question_parser.add_argument('question_statement',type=str,required=True,help='question_statementis required')
Question_parser.add_argument('quiz_id',type=int,required=True,help= 'quiz_id is required')
Question_parser.add_argument('option1',type=str, required=True,help='option_1 is required')
Question_parser.add_argument('option2',type=str, required=True,help='option_2 is required')
Question_parser.add_argument('option3',type=str, required=True,help='option_3 is required')
Question_parser.add_argument('option4',type=str, required=True,help='option_4 is required')
Question_parser.add_argument('correct_option',type=str,required=True,help='correct_option is required')
Question_parser.add_argument('no_question',type=int,required=True,help="total number of question is required")

# 6.Score Table

Score_parser=reqparse.RequestParser()
Score_parser.add_argument("score",type=int,required=True,help='scores is required')
Score_parser.add_argument("date",type=int,required=True,help='date is required')
Score_parser.add_argument("user_id",type=int,required=True,help='userid is required')
Score_parser.add_argument("subject_id",type=int,required=True,help='subid is required')
Score_parser.add_argument("chapter_id",type=int,required=True,help='chapterid is required')
Score_parser.add_argument("quizID",type=int,required=True,help='quizid is required')


class ChapterQuiz(Resource):
    def get(self,chapter_id=None):
        if chapter_id:
            quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
            return [{
                "quiz_id":quiz.quiz_id,
                "duration":quiz.duration,
                "marks":quiz.marks,
                "date":quiz.date,
                "quiz_name":quiz.quiz_name
                }
                
                for quiz in quizzes

            ]
        
        else:
            return {"message":"no chapter quiz has found"},400
        
#-----------------------------------------------------------------------------------------------------------------------------------------------------#

class QuizAPI(Resource):
    def get(self,Quiz_id=None):
        if Quiz_id:
            quiz=Quiz.query.get(Quiz_id)
            if quiz:
                return {
                    "date":quiz.date,
                    "duration":quiz.duration,
                    "chapter_id":quiz.chapter_id,
                    "quiz_id":quiz.quiz_id,
                    "marks":quiz.marks,
                    "quiz_name":quiz.quiz_name
                }
        all_quiz=Quiz.query.all()
        return [{
            "duration":quiz.duration,
            "chapter_id":quiz.chapter_id,
            "date":quiz.date,
            "marks":quiz.marks,
            "quiz_id":quiz.quiz_id,
            "quiz_name":quiz.quiz_name


        }for quiz in all_quiz
        ]
    def post(self):
        
        args=Quiz_parser.parse_args()

        quiz=Quiz(
            duration=args["duration"],
            date=args["date"],
            chapter_id=args["chapter_id"],
            marks=args["marks"],
            quiz_name=args["quiz_name"]

        )
        db.session.add(quiz)
        db.session.commit()
        return "quiz details added successfully"
    
    def put(self,quiz_id="None"):
        if quiz_id:
            quiz=Quiz.query.get(quiz_id)
            args=Quiz_parser.parse_args
            if quiz:
               quiz.date=args["date"]
               quiz.marks=args["marks"]
               quiz.duration=args["duration"]
               quiz.chapter_id=args["chapter_id"]
               quiz.quiz_name=args["quiz_name"]
               db.session.commit()
               return {"message": "quiz updated successfully"}, 200
        return {"message": "quiz not found"}, 400
            

    def delete(self,quiz_id="None"):
        if quiz_id:
            quiz=Quiz.query.get(quiz_id)
            if quiz:
                db.session.delete(quiz)
                db.session.commit()
                return {"message": "quiz deleted successfully"}, 200
            return {"message": "quiz  not found"}, 400


#-----------------------------------------------------------------------------------------------------------------------------------------------------#
class QuizQuestionsAPI(Resource):
    def get(self,quiz_id=None):

        if quiz_id:
            questions= Question.query.filter_by(quiz_id=quiz_id).all()
            return [
                {
                    "question_id":question.question_id,
                    "question_title":question.question_title,
                    "question_statement":question.question_statement,
                    "option1" : question.option1,
                    "option2" : question.option2 ,
                    "option3" : question.option3 , 
                    "option4" : question.option4,                                                  
                    "correct_option":question.correct_option,
                    "no_question":question.no_question                                                  
                } for question in questions                                                                                                    
            ],200
        
        
# ---------------------------------------------------------------------


class SubjectChaptersAPI(Resource):
    def get(self, subject_id=None):
        
        if subject_id:
            chapter = Chapter.query.filter_by(subject_id=subject_id).all()
        return [
            {
                "chapter_id": chapter.chapter_id,  # Use chapter_id
                "description": chapter.description,
                "subject_id": chapter.subject_id,
                "user_id": chapter.user_id,
                "chapter_name":chapter.chapter_name
            }
            for chapter in chapter
        ], 200
    
class ChaptersAPI(Resource):
    def get(self, chapter_id=None):
        
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if chapter:
                return {
                    "chapter_id": chapter.chapter_id,  # Use chapter_id
                    "description": chapter.description,
                    "subject_id": chapter.subject_id,
                    "user_id": chapter.user_id,
                    "chapter_name":chapter.chapter_name
                }, 200
            return {"message": "Chapter not found"}, 400

        all_chapters = Chapter.query.all()
        return [
            {
                "chapter_id": chapter.chapter_id,  # Use chapter_id
                "description": chapter.description,
                "subject_id": chapter.subject_id,
                "user_id": chapter.user_id,
                "chapter_name":chapter.chapter_name
            }
            for chapter in all_chapters
        ], 200

    def post(self):
        args = chapter_parser.parse_args()
        new_chapter = Chapter(
            description=args["description"],
            subject_id=args["subject_id"],
            user_id=args["user_id"],
            chapter_name=args["chapter_name"]
        )
        db.session.add(new_chapter)
        db.session.commit()
        return {"message": "Chapter added successfully", "chapter_id": new_chapter.chapter_id}, 201  # Return chapter_id

    def put(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        args = chapter_parser.parse_args()
        if chapter:
            chapter.description = args["description"]
            chapter.subject_id = args["subject_id"]
            chapter.user_id = args["user_id"]
            chapter.name=args["chapter_name"]
            db.session.commit()
            return {"message": "Chapter updated successfully"}, 200
        return {"message": "Chapter not found"}, 404

    def delete(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if chapter:
            db.session.delete(chapter)
            db.session.commit()
            return {"message": "Chapter deleted successfully"}, 200
        return {"message": "Chapter not found"}, 404


#-----------------------------------------------------------------------------------------------------------------------------------------------------#


class SubjectsAPI(Resource):
    def get(self,subject_id=None):
        if subject_id:
            subject=Subjects.query.get(subject_id)
            if subject:
                subject_data = {
                    "subject_id":subject.subject_id,
                    "subject_name":subject.subject_name,
                    "description":subject.description,
                    "user_id": subject.user_id

                }
                return subject_data,200
            else:
                return{"message":"subject not found"},400
        
        else:
            all_subjects=Subjects.query.all()
            subjects=[
                {
                    "subject_id":subject.subject_id,
                    "subject_name":subject.subject_name,
                    "description":subject.description,
                    "user_id":subject.user_id
                }for subject in all_subjects
            ]
            return subjects ,200
    

    def post(self):
        args=Subjects_parser.parse_args()
        new_subject= Subjects(
            subject_name=args["subject_name"],
            description=args["description"],
            user_id=args["user_id"]
        )

        db.session.add(new_subject)
        db.session.commit()
        return {"message": "subject added successfully", "subject_id": new_subject.subject_id}, 200

    def put(self, subject_id):
        args = Subjects_parser.parse_args()
        subject = Subjects.query.get(subject_id)
        if subject:
            subject.subject_name=args["subject_name"]
            subject.description=args["description"]
            subject.user_id=args["user_id"]
            db.session.commit()
            return {"message": f"User with ID {subject_id} updated successfully"}, 200
        else:
            return {"message": f"User with ID {subject_id} not found"}, 400
    
    def delete(self, subject_id):
        subject_to_delete = Subjects.query.get(subject_id)
        if subject_to_delete:
            db.session.delete(subject_to_delete)
            db.session.commit()
            return {"message": f"User with ID {subject_to_delete} deleted successfully"}, 200
        else:
            return {"message": f"User with ID {subject_to_delete} not found"}, 400


#-----------------------------------------------------------------------------------------------------------------------------------------------------#
        

class UsersAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            user = Users.query.get(user_id)
            if user:
                user_data = {
                    "user_id": user.user_id,
                    "email": user.email,
                    "password": user.password,
                    "qualification": user.qualification,
                    "dob": user.dob,
                    "role": user.role
                }
                return user_data, 200
            else:
                return {"message": "User not found"}, 404
        else:
            all_users = Users.query.all()
            
            users_data = [
                {
                    "user_id": user.user_id,
                    "email": user.email,
                    "password": user.password,
                    "qualification": user.qualification,
                    "dob": user.dob,
                    "role": user.role
                } for user in all_users
            ]
            return users_data, 200

    def post(self):
        args = Users_parser.parse_args()
        new_user = Users(
            email=args['email'],
            password=args['password'],
            qualification=args['qualification'],
            dob=args.get('dob'),  
            role=args.get('role', "user")  
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User added successfully", "user_id": new_user.user_id}, 201

    def put(self, user_id):
        args = Users_parser.parse_args()
        user = Users.query.get(user_id)
        if user:
            user.email = args['email']
            user.password = args['password']
            user.qualification = args['qualification']
            user.dob = args['dob']
            user.role = args['role']
            db.session.commit()
            return {"message": f"User with ID {user_id} updated successfully"}, 200
        else:
            return {"message": f"User with ID {user_id} not found"}, 404

    def delete(self, user_id):
        user_to_delete = Users.query.get(user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return {"message": f"User with ID {user_id} deleted successfully"}, 200
        else:
            return {"message": f"User with ID {user_id} not found"}, 404

#-----------------------------------------------------------------------------------------------------------------------------------------------------#

class QuestionAPI(Resource):
    def get(self, question_id=None):
        if question_id:
            question = Question.query.get(question_id)
            if question:
                return {
                    "quiz_id": question.quiz_id,
                    "question_id": question.question_id,
                    "question_title": question.question_title,
                    "question_statement": question.question_statement,
                    "option1": question.option1,
                    "option2": question.option2,
                    "option3": question.option3,
                    "option4": question.option4,
                    "correct_option": question.correct_option,
                    "no_question": question.no_question

                }, 200
            return {"message": "Question not found"}, 404

        all_questions = Question.query.all()
        return [
            {
                "quiz_id": question.quiz_id,
                "question_id": question.question_id,
                "question_title": question.question_title,
                "question_statement": question.question_statement,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
                "correct_option": question.correct_option,
                "no_question": question.no_question
            }
            for question in all_questions
        ], 200

    def post(self):
        args = Question_parser.parse_args()
        new_question = Question(
            question_title=args["question_title"],
            question_statement=args["question_statement"],
            quiz_id=args["quiz_id"],
            option1=args["option1"],
            option2=args["option2"],
            option3=args["option3"],
            option4=args["option4"],
            correct_option=args["correct_option"],
            no_question=args["no_question"]

        )
        db.session.add(new_question)
        db.session.commit()
        return {"message": "Question added successfully", "question_id": new_question.question_id}, 201

    def put(self, question_id):
        question = Question.query.get(question_id)
        if question:
            args = Question_parser.parse_args()
            question.question_title = args["question_title"]
            question.question_statement = args["question_statement"]
            question.option1 = args["option1"]
            question.option2 = args["option2"]
            question.option3 = args["option3"]
            question.option4 = args["option4"]
            question.correct_option = args["correct_option"]
            question.no_question = args["no_question"]
            question.quiz_id=args["quiz_id"]

            db.session.commit()
            return {"message": "Question updated successfully"}, 200
        return {"message": "Question not found"}, 404

    def delete(self, question_id):
        question = Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            return {"message": "Question deleted successfully"}, 200
        return {"message": "Question not found"}, 404

#-----------------------------------------------------------------------------------------------------------------------------------------------------#

class ScoreAPI(Resource):
    def get(self, id=None):
        if id:
            score = Score.query.get(id)
            if score:
                return {
                    "id": score.id,
                    "score": score.score,
                    "date": score.date,
                    "user_id": score.user_id,
                    "subject_id": score.subject_id,
                    "chapter_id": score.chapter_id,
                    "quizID":score.quizID
                }, 200
            return {"message": "Score not found"}, 404

        all_scores = Score.query.all()
        return [
            {
                "id": score.id,
                "score": score.score,
                "date": score.date,
                "user_id": score.user_id,
                "subject_id": score.subject_id,
                "chapter_id": score.chapter_id,
                "quizID":score.quizID
            }
            for score in all_scores
        ], 200

    def post(self):
        args = Score_parser.parse_args()
        new_score = Score(
            score=args["score"],
            date=args["date"],
            user_id=args["user_id"],
            subject_id=args["subject_id"],
            chapter_id=args["chapter_id"],
            quizID=args["quizID"]
        )
        db.session.add(new_score)
        db.session.commit()
        return {"message": "Score added successfully", "id": new_score.id}, 201

    def put(self, id):
        score = Score.query.get(id)
        if score:
            args = Score_parser.parse_args()
            score.score = args["score"]
            score.date = args["date"]
            score.user_id = args["user_id"]
            score.subject_id = args["subject_id"]
            score.chapter_id = args["chapter_id"]
            score.quizID=args["quizID"]
            db.session.commit()
            return {"message": "Score updated successfully"}, 200
        return {"message": "Score not found"}, 404

    def delete(self, id):
        score = Score.query.get(id)
        if score:
            db.session.delete(score)
            db.session.commit()
            return {"message": "Score deleted successfully"}, 200
        return {"message": "Score not found"}, 404


#-----------------------------------------------------------------------------------------------------------------------------------------------------#





def initialize_api(api):
    api.add_resource(UsersAPI, "/API/Users", "/API/Users/<int:user_id>")
    api.add_resource(SubjectsAPI, "/API/Subjects", "/API/Subjects/<int:subject_id>")
    api.add_resource(ChaptersAPI,"/API/Chapters","/API/Chapters/<int:chapter_id>")
    api.add_resource(QuizAPI,"/API/Quiz","/API/Quiz/<int:quiz_id>")
    api.add_resource(QuestionAPI,"/API/Questions","/API/Question/<int:question_id>")
    api.add_resource(ScoreAPI,"/API/Score","/API/Score/<int:id>")
    api.add_resource(SubjectChaptersAPI,"/API/SubjectChapters","/API/SubjectChapters/<int:subject_id>")
    api.add_resource(ChapterQuiz,"/API/ChapterQuiz","/API/ChapterQuiz/<int:chapter_id>")
    api.add_resource(QuizQuestionsAPI,"/API/QuizQuestions","/API/QuizQuestions/<int:quiz_id>")
    