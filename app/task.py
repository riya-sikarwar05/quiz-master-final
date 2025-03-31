from flask import session
import requests
import json
API_BASE_URL = "http://localhost:5000/API"

def logout():
    session['admin_id'] = None
    session['user_id'] = None
    
def handleCSV():
    import pandas as pd
    df = pd.read_csv('uploads/upload.csv')
    quizID = session.get('quizID', None)
    for index, row in df.iterrows():
        data = row.to_dict()
        print(f"Row {index}: {json.dumps(data, indent=4)}")  # Print row data

        quizQuestion = {
            "question_title": str(data.get('question_title', '')),
            "question_statement": str(data.get('question_statement', '')),
            "quiz_id": int(quizID) if quizID and str(quizID).isdigit() else None,
            "option1": str(data.get('option1', '')),
            "option2": str(data.get('option2', '')),
            "option3": str(data.get('option3', '')),
            "option4": str(data.get('option4', '')),
            "correct_option": str(data.get('correct_option', '')),
            "no_question": int(data.get('no_question', 1)) if pd.notna(data.get('no_question')) and str(data['no_question']).isdigit() else 1
        }

        print(f"Prepared quizQuestion: {json.dumps(quizQuestion, indent=4)}")  # Print formatted request payload
        
        response = requests.post(API_BASE_URL+'/Questions', json=quizQuestion)

        if response.status_code == 201:
            print(f"User created successfully: {response.json()}")
        else:
            print(f"Failed to create question. Response: {response.text}")