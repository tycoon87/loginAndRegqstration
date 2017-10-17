from flask import Flask, render_template,session, flash, request, redirect
import re

from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'WhereAreYouDoing'
mysql = MySQLConnector(app,'regastration')

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def regaster():
        session['firstName'] = ''
        session['lastName'] = ''
        session['birthdate'] = ''
        session['email'] = ''
        session['password'] = ''
        session['confirmPassword'] = ''
        session['loggedIn'] = ''
        return render_template('/register.html')

@app.route('/submit', methods = ['POST'])
def submit():
    print "inside submit"
    query = "select * from user"
    userdb = mysql.query_db(query)
    putinto = "INSERT INTO user (email, firstName,lastName,  screenName, timeStamp, password) VALUES (:email, :firstName, :lastName, :screenName, NOW(), :password)"
    data = {
        'email': request.form['email'],
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'screenName': request.form['screenName'],
        'password': request.form['password'],
        }
    addressToVerify = request.form["email"]
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

    emailquery = "select email from user"
    
    if request.form['email'] != request.form['confermPassword']:
        flash('password dose not mach', 'passwordError')
    
    if request.form['email'] == "email":
        flash('Email already in use', 'emailError')
    
    if request.form['email'] == '':
        flash('Email cannot be blank', 'emailError')
    else:
        session['email'] = request.form['email']

    if request.form['firstName'] == '':
        flash('First Name cannot be blank', 'firstNameError')
    else:
        session['firstName'] = request.form['firstName']
    
    if request.form['lastName'] == '':
        flash('Last Name cannot be blank', 'lastNameError')
    else:
        session['lastName'] = request.form['lastName']
    
    if request.form['screenName'] == '':
        flash('screen Name cannot be blank', 'screenNameError')
    else:
        session['screenName'] = request.form['screenName']
    
    if request.form['password'] == '':
        flash('password cannot be blank', 'passwordError')
    else:
        session['password'] = request.form['password']
        
    if session['loggedIn'] == '':
        session['loggedIn'] = 'true'
        
    
    if match == None:
        return redirect('/register')

    
        return redirect('/register')

    elif mysql.query_db(putinto, data):
        email = request.form['email']
        session['email'] = email
        
        firstName = request.form['firstName']
        session['firstName'] = firstName
        
        lastName = request.form['lastName']
        session['lastName'] = lastName
        
        screenName = request.form['screenName']
        session['screenName'] = screenName
        
        password = request.form['password']
        session['password'] = password
        return redirect ("/sucsess")
    
@app.route('/sucsess' )
def sucsess():
#    query
#    userdb = mysql.query_db(query)

    return render_template("/sucsess.html")
    
@app.route('/login', methods=['Post'])
def login():
    print "poop"
#    attemps = 0
    email = request.form['email']
    print email
    query = "SELECT * FROM user WHERE email = '" + request.form['email'] +"'"
    print query
    userdb = mysql.query_db(query)
    print userdb
    print 'poop'
    if userdb == request.form['email'] and userdb == request.form['password']:
        print session['logged_in'], session['email'], session['firstName'], session['lastName'], session['screenName'], "poop"
        session['logged_in'] = 'True'
        session['email'] = 'email'
        session['firstName'] = 'firstName'
        session['lastName'] = 'lastName'
        session['screenName'] = 'screenName'
        print 'poop'  
        return render_template("/sucsess.html")
    print 'poop'   
#    elif userdb != request.form['email'] or != request.form['password']:
#        print 'poop'
#        flash('wrong password!')
#        attemps += 1
#        return redirect('/')
#    print 'poop'
    
@app.route('/logout')
def logout():
    session['first_name'] = ''
    session['last_name'] = ''
    session['email'] = ''
    session['password'] = ''
    session['confirm_password'] = ''
    session['userid'] = ''
    session['loggedin'] = 'False'

    return redirect('/')
    

app.run(debug=True)