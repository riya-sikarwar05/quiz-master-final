import smtplib
def emailtrigger():
    email = "gnspdc@gmail.com"
    reciever_email = "sikarwarr.riyaa@gmail.com"

    subject =  "The score mentioned for the courses"
    message =  "tomorrow is MATH EXAM " 
    
    

    text = f"subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()

    server.login(email,"kagxjqoxjxswdzcw")
    server.sendmail(email, reciever_email,text)
    print("email has been sent to" + reciever_email)



from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def emailtriggerPDF():
    sender_email = "gnspdc@gmail.com"
    receiver_email = "sikarwarr.riyaa@gmail.com"  # fixed typo 'gmal.com'
    password = "kagxjqoxjxswdzcw"

    subject = "your Score in this month"
    body = "Please find the attached PDF for the Exams."

    # Create email message
    msg = MIMEMultipart()
    msg['From'] =  "gnspdc@gmail.com"
    msg['To'] = "sikarwarr.riyaa@gmail.com"
    msg['Subject'] ="pdf of scores"

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

   # Attach the PDF file
    pdf_path = "/home/riya/celeryBeatmad2/quiz-master-final/download/random_scores.pdf"  # Correct full path
    with open(pdf_path, "rb") as pdf_file:
        part = MIMEApplication(pdf_file.read(), Name="random_scores.pdf")
        part['Content-Disposition'] = f'attachment; filename="random_scores.pdf"'
        msg.attach(part)
        print("hi")

    # Sending the em    pdf_path = "/home/riya/celeryBeatmad2/quiz-master-final/download/random_scores.pdf"  # Correct full path
    with open(pdf_path, "rb") as pdf_file:
        part = MIMEApplication(pdf_file.read(), Name="random_scores.pdf")
        part['Content-Disposition'] = f'attachment; filename="random_scores.pdf"'
        msg.attach(part)
        print("hi")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("gnspdc@gmail.com", "kagxjqoxjxswdzcw")
        server.sendmail('gnspdc@gmail.com', "sikarwarr.riyaa@gmail.com", msg.as_string())
        server.quit()
        print("hi")
    except Exception as e:
        print(f"Error: {e}")


emailtriggerPDF()
# Call the function
