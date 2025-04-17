import requests
from flask import render_template, request, jsonify, abort, redirect, url_for, session, send_from_directory
from app import app
API_BASE_URL = "http://localhost:5000/API"  # Change this if the API runs on a different port .
from .task import handleCSV
import os
from werkzeug.utils import secure_filename
from flask_caching import Cache
from .utils import send_pdf_to_users, pdfReport
from .models import ScoreView, db
from flask_caching import Cache
from app.mail import emailtrigger
from app.mail import emailtriggerPDF



config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache", 
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": 'mycache'
}

app.config.from_mapping(config)
cache = Cache(app)


# Configure upload folder and allowed file types
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "your_secret_key"

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# db.init_app(app)

@app.route('/scores')
def scores():
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    query = ScoreView.query

    if search_query:
        query = query.filter(
            (ScoreView.user_name.ilike(f"%{search_query}%")) |
            (ScoreView.subject_name.ilike(f"%{search_query}%")) |
            (ScoreView.chapter_name.ilike(f"%{search_query}%")) |
            (ScoreView.quiz_name.ilike(f"%{search_query}%"))
        )

    if order == 'desc':
        query = query.order_by(db.desc(getattr(ScoreView, sort_by)))
    else:
        query = query.order_by(getattr(ScoreView, sort_by))

    scores = query.all()
    
    return render_template('scores.html', scores=scores, search_query=search_query, sort_by=sort_by, order=order)

# Function to check allowed file type
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/AdminQuestion/<int:quiz_id>')
def AdminQuestion(quiz_id):
    session['quizID'] = quiz_id
    return render_template("admin-file-upload.html")


@app.route('/UserQuestion/<int:quiz_id>')
def UserQuestion(quiz_id):
    session['quizID'] = quiz_id
    return render_template("userQuestion.html")



@app.route("/admin/statistics")
@cache.cached(timeout=600)
def admin_statistics():
    return render_template("admin-statistics.html")

@app.route('/download/<filename>')
def download_file(filename):
    download_folder = os.path.join(app.root_path, '../download')  # Correct path reference
    return send_from_directory(download_folder, filename, as_attachment=True)
# Route to render the file upload page
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"message": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"message": "No selected file"}), 400
        print(file.filename)

        if file and allowed_file(file.filename):
            filename = "upload.csv"  # Set filename to upload.csv
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            
            # Save the file, replacing existing upload.csv if it exists
            file.save(file_path)
            handleCSV()
            return jsonify({"message": "File uploaded successfully as upload.csv!"}), 200

        return jsonify({"message": "Invalid file type. Only CSV files are allowed!"}), 400

    # Render the upload page for GET requests
    return render_template("admin-file-upload.html")


@app.route("/", methods=["GET", "POST"])
def start():
    return render_template("login.html")

@app.route("/admin-login", methods=["GET", "POST"])
def adminLogin():
    if 'admin_id' in session:
        return redirect(url_for("AdminDashboard"))
    if request.method == 'POST':
        data = request.form.to_dict()
        response = requests.get(f"{API_BASE_URL}/Users")
        if response.status_code == 200:
        
            users = response.json()
            email_present=False 
            user_data=""
            for user in users:
                if data["email"]==user["email"]:
                    email_present=True
                    user_data=user


            if email_present:    
                if user_data["password"] == data["password"] and user_data["role"] == "admin":
                    session['admin_id'] = user_data["user_id"]
                    return redirect(url_for("AdminDashboard"))
                else:
                    return render_template("admin-login.html", error="Wrong Password")
        return render_template("admin-login.html", error="No user with this Username")
    return render_template("admin-login.html")

@app.route("/user-login", methods=["GET", "POST"])
def userLogin():
    if 'user_id' in session:
        return redirect(url_for("UserDashboard"))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        response = requests.get(f"{API_BASE_URL}/Users")  # Fetch all users
        if response.status_code == 200:
            users = response.json()  # This is a list
            user = next((u for u in users if u["email"] == data["email"]), None)  # Find user by email
            print(user)
            if user and user["password"] == data["password"] and user["role"] == "user":
                session['user_id'] = user["user_id"]
                return render_template("user-dashboard.html")
            else:
                return render_template("user-login.html", error="Wrong Username or Password")
    
        return render_template("user-login.html", error="No user with this Username")
    
    return render_template("user-login.html")


@app.route("/register", methods=["GET", "POST"])
def userRegister():
    if 'user_id' in session:
        return redirect(url_for("UserDashboard"))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        response = requests.get(f"{API_BASE_URL}/Users")  # Fetch all users
        if response.status_code == 200:
            users = response.json()
            if any(user["email"] == data["email"] for user in users):
                return render_template("user-login.html", error="User already registered, please login!")

        user_data = {
            "email": data['email'],
            "password": data['password'],
            "qualification": data['qualification'],
            "dob": data['dob'],
            "role": "user"
        }
        
        response = requests.post(API_BASE_URL+'/Users', json=user_data)
        
        if response.status_code == 201:
            return redirect(url_for('userLogin'))
        
        return render_template("user-register.html", error=f"Registration failed! Error: {response.text}")  # Log the error
    
    return render_template("user-register.html")

@app.route("/user-dashboard",methods=["GET","POST"])
def UserDashboard():
        
    if 'user_id' not in session:
        return redirect(url_for("userLogin"))  # Redirect if not logged in
    
    # response = requests.get(f"{API_BASE_URL}/Subjects")
    # print(response.json())
    return render_template("user-dashboard.html")

@app.route("/admin-subject",methods=["GET","POST"])
def AdminDashboard():
    return render_template("admin-subject.html")

@app.route("/admin-new-subject",methods=["GET","POST"])
def admin_new_subject():

    return render_template("admin-add-subject.html")


@app.route("/logout")
def logout():
    session.pop('admin_id', None)
    session.pop('user_id', None)

    return redirect(url_for("start"))

@app.route("/AddChapter/<int:subject_id>",methods=["POST","GET"])
def add_chapter(subject_id):
    if request.method == 'POST':

        try:
            print(data)
            data=request.get_json()
            print(data)

            chapter_data={
            "chapter_name":data["Chapter_name"],
            "description":data["description"],
            "user_id": session['admin_id'],
            "subject_id": "4"
            }

            response=requests.post(f"{API_BASE_URL}/Chapters",json=chapter_data)
            print("resposne",response.json())
            print("status code",response.status_code)
            print("chapter posted succesfully")
            return render_template("admin-chapter.html")

        except Exception as e:
            return {"error": "Server error", "message": str(e)}, 500 

    
    return render_template("admin-chapter.html")


@app.route("/Add-Chapter",methods=["POST","GET"])
def addChapter():
    if request.method == 'POST':
        # print(request.get_json())

        try:
            data=request.get_json()

            chapter_data={
            "chapter_name":data["Chapter_name"],
            "description":data["description"],
            "user_id": session['admin_id'],
            "subject_id": data["subject_id"]
            }

            response=requests.post(f"{API_BASE_URL}/Chapters",json=chapter_data)
            print("resposne",response.json())
            print("status code",response.status_code)
            print("chapter posted succesfully")
            return render_template("admin-chapter.html")

        except Exception as e:
            return {"error": "Server error", "message": str(e)}, 500 

    
    return render_template("admin-chapter.html")

@app.route('/AddAdminQuiz',methods=["POST"])
def AddAdminQuiz():
    try:
        data=request.get_json()
        print("RECIEVED DATA:",data)
        print("----------------------------")
        quiz_data={
            "duration":data['duration'],
            "date":data["date"],
            "marks":data["marks"],
            "chapter_id":data["chapter_id"],
            "quiz_name":data["quiz_name"]
        }

        print("----------------------------")
        print("Quiz data:",quiz_data)
        response=requests.post(API_BASE_URL+'/Quiz', json=quiz_data)
        print("Response:", response.json())
        print("Status code:", response.status_code)
        print("Data posted successfully")
        print(session)
        return redirect(url_for("AdminQuiz"))

    except Exception as e:
        return {"error": "Server error", "message": str(e)}, 500 
      

@app.route("/AddSubject", methods=["POST"])
def add_subject():
    
    try:
        data = request.get_json()
        print("Received data:", data)

        subject_data = {
            "subject_name": data['subject_name'],
            "description": data['description'],
            "user_id": session['admin_id']
        }
        
        response = requests.post(API_BASE_URL+'/Subjects', json=subject_data)
        print("Response:", response.json())
        print("Status code:", response.status_code)
        print("Data posted successfully")
        print(session)
        return redirect(url_for("AdminDashboard"))

    except Exception as e:
        return {"error": "Server error", "message": str(e)}, 500 
        

@app.route('/subjectTest')
def subject_test():
    return render_template('subjectTest.html')

@app.route('/UserChapters/<int:subject_id>')
def UserChapters(subject_id):
    session['subject_id'] = subject_id
    return render_template("user-chapter.html")

@app.route('/Quiz')
def Quiz():
    return render_template("Quiz.html")
                
@app.route('/AdminQuiz/<int:chapter_id>')
def AdminQuiz(chapter_id):
    return render_template("admin-quiz.html")

@app.route('/userQuiz/<int:chapter_id>')
def userQuiz(chapter_id):
    session['chapter_id'] = chapter_id
    return render_template("user-quiz.html")

@app.route("/scoreData", methods=["POST", "GET"])
def scoreData():
    if request.method == 'POST':
        print(request.get_json())

        try:
            data = request.get_json()

            score = {
                "score": data["score"],
                "chapter_id": session.get('chapter_id'),  # Use `get()` to avoid KeyError
                "date": 0,
                "user_id": session.get('user_id'),
                "quizID": session.get('quizID'),
                "subject_id": session.get('subject_id')
            }

            print("Score Data:", score)

            response = requests.post(f"{API_BASE_URL}/Score", json=score)

            print("Response:", response.json())
            print("Status Code:", response.status_code)

            if response.status_code == 201:
                print("Chapter posted successfully")
                return redirect(url_for("userQuiz"))
            else:
                return jsonify({"error": "Failed to post score", "details": response.json()}), response.status_code

        except Exception as e:
            print("Error:", str(e))  # Log the actual error
            return jsonify({"error": "An error occurred", "details": str(e)}), 500  # Return an actual error response

    return jsonify({"message": "GET method not allowed"}), 405  # Return a response for GET requests

@app.route("/mailtrigger")
def mailtrigger():
    emailtrigger()
    return render_template("admin-statistics.html")

@app.route("/mailtriggerPDF")
def mailtriggerPDF():
    emailtriggerPDF()
    return render_template("admin-quiz.html")

@app.route("/userQUIZES")
def userQUIZES():
    return render_template("userQUIZES.html")
