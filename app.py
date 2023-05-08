from flask import Flask, redirect, request, render_template, flash, url_for,session
from datetime import datetime
import datetime as dt
import os
import json
import pymongo
import pandas as pd
import numpy as np
import pickle
#import requests
import urllib.request

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from email.message import EmailMessage



client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.s3ywdpg.mongodb.net/?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.lysk5le.mongodb.net/?retryWrites=true&w=majority")
# db = client.Farud_detection
db = client["Calendar"]
event=db["event"]
event1=db["event1"]
c1 = db["users"]
c2 = db["files"]
user_name=''
flag1 = 0

def fun():
    record1=[]
    dbResponse=list(db[str(user_name)].find({},{'_id': 0}))
    #print(dbResponse)
    #print(type(dbResponse))
    for record in dbResponse:
        #record.popitem()
        record1.append({
            "events":record['events'],
            "day":record['day'],
            "month":record['month'],
            "year":record['year']
            
            })
        #print(record1)
        #print(type(record1))
    return record1


EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['indiafiberone@gmail.com', 'test@example.com']

msg = EmailMessage()
msg['Subject'] = 'Notification Mail'
msg['From'] = "sivak163@gmail.com"
msg['To'] = "indiafiberone@gmail.com"

msg.set_content('This is a plain text email')

msg.add_alternative("""\
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <div>
    <p>Hello Greeting for the day <br> Your event name Yoga is scheduled from 8:30 PM - 9:30 PM
</p>
        <table>
            <tr>
                <th>
                    <ul>
                    <a style="text-decoration: none;color: #fff;font-weight: bold;font-size: 20px;cursor: pointer;width: 100px;margin: 5px;padding: 13px;border-radius: 18px;background-color: rgb(17, 134, 36);"
                    href="http://192.168.0.23:8000/mail?&name=test@gmail.com">Yes</a>
                    </ul>
                </th>
                <th>
                    <ul>
                    <a style="text-decoration: none;color: #fff;font-weight: bold;font-size: 20px;cursor: pointer;width: 100px;margin: 5px;padding: 13px;border-radius: 18px;background-color: rgb(167, 38, 28);"
                    href="">No</a>
                    </ul>
                </th>
                <th>
                    <ul>
                    <a style="text-decoration: none;color: #fff;font-weight: bold;font-size: 20px;cursor: pointer;width: 100px;margin: 5px;padding: 13px;border-radius: 18px;background-color: rgb(11, 168, 196);"
                    href="http://192.168.0.23:8000/mail/Reschedule">Reschedule</a>
                    </ul>
                </th>
            </tr>
        </table>
    </div>
</body>
</html>
""", subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login("sivak163@gmail.com", "yztzqrvrngkedwge")
    smtp.send_message(msg)
    print('notification mail sent Sucessfully')
    
def sendemail(s_email,event,time):
    #----------- Sender mail----------------
    msg = MIMEMultipart()
    msg['From'] = "sivak163@gmail.com"
    msg['To'] = s_email
    msg['Subject'] = "This is Remainder for the Events "
    body = "Hello Greeting for the day \n Your event name "+str(event)+" is scheduled from  "+str(time)+" Do bring laptop for this event"
    time= str(time).replace(" ", "%20")
    body1="Remainder"+str(event)+"at"+str(time)+"Bring%20Things"
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sivak163@gmail.com", "yztzqrvrngkedwge")
    text = msg.as_string()
    s.sendmail("sivak163@gmail.com", s_email, text)
    s.quit()
    print('mail sent Sucessfully')
    urllib.request.urlopen('https://www.fast2sms.com/dev/bulkV2?authorization=uEXyjpio5NjLERWLSciOMnyk1s7MZ4qtdCoKehIiKXAgeXVJ5Xgad6E7sqiU&route=v3&sender_id=Cghpet&message='+body1+'&language=english&flash=0&numbers=7530079684')
    #response = requests.get('https://www.fast2sms.com/dev/bulkV2?authorization=uEXyjpio5NjLERWLSciOMnyk1s7MZ4qtdCoKehIiKXAgeXVJ5Xgad6E7sqiU&route=v3&sender_id=Cghpet&message='+body+'&language=english&flash=0&numbers=6381263623', headers=headers)
    print('Msg sent Sucessfully')#7530079684
def mailcheck():
    global user_name
    now = datetime.now()
    today=str(now.day)
    #print(today)
    listItem=list(db[str(user_name)].find({'day':int(today)}))
    for Item in listItem:
        for j in range(len(Item['events'])):
            print(Item['events'][j]['time'])
            list2 = Item['events'][j]['time'].split('-')
            list11=str(list2[0]).replace(" ", "")
            start_time = list11
            now = datetime.now() # current date and time
            date_time = now.strftime("%H:%M:%S")
            end_time = date_time
            t1 = datetime.strptime(start_time, "%I:%M%p")
            t2 = datetime.strptime(end_time, "%H:%M:%S")
            delta = t1-t2
            if (delta.total_seconds() >0 and delta.total_seconds() <=1800):
                sendemail(str(user_name),Item['events'][j]['title'],Item['events'][j]['time'])
            else:
                print('nomail')
            #print(f"Time difference is {delta.total_seconds()} seconds")

app = Flask(__name__)


@app.route('/')
def home_page():
    print('1')
    return render_template('landing.html', ok='run')


@app.route('/signin', methods=['GET', 'POST'])
def login_page(title='Login Demo'):
    global msgs, error,user_name
    error = []
    if request.method == 'GET':
        return render_template('landing.html', ok='run')

    elif request.method == 'POST':
        print('3')
        print(request.form['email'], request.form['password'])
        item_details = c1.find({"email": request.form['email']})
        for item in item_details:
            if request.form['email'] == item['email'] and request.form['password'] == item['password']:
                msgs = 'Login Successfuly'
                user_name=request.form['email']
                #print(type(user_name))
                print("flash")
                
                return render_template('landing.html', msgs=msgs,user_name=user_name, ok='ok')
          
        error = 'Email or Password Incorrect'
        print(error)
        return render_template('landing.html', error=error, ok='run')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page(title='Signup Page'):
    global flag1, war, msgs
    error = ''
    war = ''
    msgs = ''
    user_data = {}

    if request.method == 'GET':
        flag1 = 0
        return render_template('landing.html', error=error, title=title, ok='run')

    elif request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            error = 'Password do not match'
            return render_template('landing.html', error=error, ok='run')

        if request.form['email'] != '' and request.form['fname'] != '' and request.form['lname'] != '' and request.form['password'] != '' and request.form['confirm_password'] != '':
            user_data = dict(request.form)
            #print(user_data)
            item_details = c1.find({"email": request.form['email']})
            for item in item_details:
                if request.form['email'] == item['email']:
                    war = 'Email Already Registered'
                    return render_template('landing.html', war=war,ok='run')
            if flag1 == 0:
                item_1 = {
                    "Username": user_data['fname']+user_data['lname'],
                    "email": user_data['email'],
                    "password": user_data['password'],
                    "cpassword": user_data['confirm_password']
                }
                c1.insert_one(item_1)
                msgs = 'Registration Successfully'
                return render_template('landing.html', msgs=msgs,ok='run')
@app.route('/event12', methods=['POST','GET'])
def event12():
    if request.method == 'GET':
        xa=fun()
        return render_template('index.html',alleventitem=xa,ok='ok')
    if request.method == 'POST':
        output=request.get_json()
        xa=fun()
        #print(type(xa))
        output1=output
        print(output)
        return render_template('index.html',alleventitem=xa,output1=output1,ok='ok')

@app.route('/addevent', methods=['POST'])
def addevent():
    global user_name
    output=request.get_json()
    result=json.loads(output)
    db[str(user_name)].insert_one(result)
    xa=fun()
    mailcheck()
    return render_template('index.html',alleventitem=xa,ok='ok')
@app.route('/mail', methods=['GET'])
def addevent_mail():
    global user_name
    now = datetime.now()
    today=str(now.day)
    name = request.args.get('name')
    user_name=name
    print(name)
    new_user={
      "Username": "",
      "email": user_name,
      "password": "1234",
      "cpassword": "1234"
    }
    
    
    New_event={'day': int(now.day), 'month': int(now.month), 'year': int(now.year), 'events': [{'title': 'Yoga', 'time': '8:30 PM - 9:30 PM'}]}
    
    #Item=db[user_name].find({'day': int(now.day) or 'month': int(now.month) or 'year': int(now.year)})
    Item=db[user_name].find_one({'day': int(now.day)})
    if Item==None:
        db[str(user_name)].insert_one(New_event)
        c1.insert_one(new_user)
        xa=fun()
        return render_template('index.html',alleventitem=xa,ok='ok')
    elif Item!=None:
            flag_mail=0
            for i in Item['events']:
                flag_mail=flag_mail+1
                print(i['time'])
                if i['time']==New_event['events'][0]['time']:
                    if flag_mail==len(Item['events']):
                        print("Event Time in Not Available ")
                        xa=fun()
                        war = "Event Time in Not Available "
                        mailcheck()
                        return render_template('index.html',war=war,alleventitem=xa, ok='ok')
                else:
                    if flag_mail==len(Item['events']):
                        db[str(user_name)].update_one({'day':int(now.day)},{'$push': {'events': New_event['events'][0]}})
                        print("ok")
                        xa=fun()
                        mailcheck()
                        return render_template('index.html',alleventitem=xa,ok='ok')
    else:
        return render_template('index.html',ok='ok')
@app.route('/Reschedule_mail', methods=['GET'])
def Reschedule_mail():
    print("Reschedule Successfully")
    mailcheck()
    return


@app.route('/delete_event', methods=['POST'])
def delete_event():
    global user_name
    output=request.get_json()
    result=json.loads(output)
    data={'title':result.get('title'),'time':result.get('time')}
    Item=db[str(user_name)].find_one({'events':data})
    print(Item)
    db[str(user_name)].update_one({'day':Item['day']},{'$pull': {'events': data}})
    last_evevnt=db[str(user_name)].find_one({'day':Item['day']})
    print(last_evevnt['events'])
    if last_evevnt['events']==[]:
        db[user_name].delete_one({"_id": last_evevnt['_id']})
        xa=fun()
        return render_template('index.html',alleventitem=xa,ok='ok')
    else:
        xa=fun()
        return render_template('index.html',alleventitem=xa,ok='ok')
@app.route('/update_event', methods=['POST'])
def update_event():
    global user_name
    war = ''
    output=request.get_json()
    result=json.loads(output)
    print(result)
    data=result.get('events')
    print(data['time'])
    listItem=list(db[str(user_name)].find({'day':result.get('day')}))
    flag=0
    for Item in listItem:
        print(Item['events'])
        for i in Item['events']:
            flag=flag+1
            print(i['time'])
            if i['time']==data['time']:
                if flag==len(Item['events']):
                    print("Event Time in Not Available ")
                    xa=fun()
                    war = "Event Time in Not Available "
                    return render_template('index.html',war=war,alleventitem=xa, ok='ok')
            else:
                if flag==len(Item['events']):
                    db[str(user_name)].update_one({'day':result.get('day')},{'$push': {'events': data}})
                    print("ok")
                    xa=fun()
                    mailcheck()
                    return render_template('index.html',alleventitem=xa,ok='ok')
        else:
            print("not ok")
            return render_template('index.html',ok='ok')
        

@app.route('/logout')
def logout():
    msgs = 'Logout Successfully'
    return render_template('landing.html', msgs=msgs, ok='logout')

if (__name__ == '__main__'):
    app.secret_key = "abc123"
    app.run(host='0.0.0.0', port=8000)
    #app.run()
