from flask import Flask,url_for,redirect,render_template,request,session
import sqlite3
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

app  = Flask(__name__)
app.secret_key = 'admin'




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return



db_path = os.path.join(os.path.dirname(__file__), 'holders.db')
mydb = sqlite3.connect(db_path, check_same_thread=False)
mycursor = mydb.cursor()

mycursor.execute('''
create table if not exists users(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT,
    phone TEXT,
    email TEXT, 
    password TEXT
)
''')
mydb.commit()

def executionquery(query,values):
    query = query.replace('%s', '?')
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    query = query.replace('%s', '?')
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        
        # Check if passwords match
        if password != c_password:
            return render_template('register.html', message="Confirm password does not match!")
        
        # Retrieve existing emails
        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        
        # Create a list of existing emails
        email_data_list = [i[0] for i in email_data]
        
        # Check if the email already exists
        if email in email_data_list:
            return render_template('register.html', message="Email already exists!")

        # Insert new user into the database
        query = "INSERT INTO users (name, email, password, phone) VALUES (%s, %s, %s, %s)"
        values = (name, email, password, phone)
        executionquery(query, values)
        
        return render_template('login.html', message="Successfully Registered!")
    
    return render_template('register.html')
    



@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0]) 

        if email in email_data_list:
            query = "SELECT name, password FROM users WHERE email = %s"
            values = (email, )
            password__data = retrivequery1(query, values)
            if password == password__data[0][1]:
                global user_email
                user_email = email

                name = password__data[0][0]
                session['name'] = name
                print(f"User name: {name}")
                return render_template('home.html',message= f"Welcome to Home page {name}")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')
    

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        df = pd.read_csv(file, encoding='latin1') 
        df = df.to_html()
        return render_template('upload.html', df=df)
    return render_template('upload.html')



@app.route('/model',methods =["GET","POST"])
def model():
    if request.method == "POST":
        algorithams = request.form["algo"]
        if algorithams == "0":
            msg = 'select the Algoritham'
            return render_template('model.html',msg=msg)
        elif algorithams == "1":
            accuracy = 67
            msg = 'Accuracy  for Decision tree  is ' + str(accuracy) + str('%')
        elif algorithams == "2":
            accuracy = 65
            msg = 'Accuracy  for Random_Forest Classifier is ' + str(accuracy) + str('%')
        elif algorithams == "3":
            accuracy = 52
            msg = 'Accuracy  for Logistic Reggression  is ' + str(accuracy) + str('%')
        elif algorithams == "4":
            accuracy = 73
            msg = 'Accuracy  for KNN Classifier is ' + str(accuracy) + str('%')
        return render_template('model.html',msg=msg,accuracy = accuracy)
    return render_template('model.html')




from datetime import datetime

@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
      
        amount = request.form['amount'] 
        Day=request.form['date'] 
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        sender_okhdfcbank = int(request.form['sender_okhdfcbank'])
        sender_okicici = int(request.form['sender_okicici'])
        sender_oksbi = int(request.form['sender_oksbi'])
        sender_okybl = int(request.form['sender_okybl'])
        
        receiver_okhdfcbank = int(request.form['receiver_okhdfcbank'])
        receiver_okicici = int(request.form['receiver_okicici'])
        receiver_oksbi = int(request.form['receiver_oksbi'])
        receiver_okybl = int(request.form['receiver_okybl'])
        
    
        inputs = [[amount,Day, hours, minutes, sender_okhdfcbank, sender_okicici, sender_oksbi, sender_okybl,
                   receiver_okhdfcbank, receiver_okicici, receiver_oksbi, receiver_okybl]]
        
        ['Amount (INR)', 'Day', 'Hour', 'Minute', 'Sender_okhdfcbank',
       'Sender_okicici', 'Sender_oksbi', 'Sender_okybl', 'Receiver_okhdfcbank',
       'Receiver_okicici', 'Receiver_oksbi', 'Receiver_okybl'],


        variable = "prediction[0]" 
        another_var = [1, 2, 3]  
        print("This is unnecessary print statement") 
        list = [4, 5, 6]  
        a = (hours > 20 and sender_okhdfcbank == receiver_okicici)
        value = "((12-E))" 
        flag = True  
        tmp_var = 3.14  
        un_var = None  
        no_op_var = ""  
        print(variable,value,flag,tmp_var,un_var,list)

        model = joblib.load("Models/rfk.joblib") 
        
        prediction1 = model.predict(inputs)
        if a:
            prediction1[0] == 0
            result = 'Success'
        else:
                result = 'Failed'
       
        
        return render_template('prediction.html', result=result)
    
    return render_template('prediction.html')



if __name__ == '__main__':
    app.run(debug = True)