from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

app.secret_key = 'riyaissmart12351426537625'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
