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
    attemps = 0
    if attemps == 5:
        return redirectct ('/lockout')
    email = request.form['email']
    data = {'email':request.form['email']}
    result = "SELECT * FROM user WHERE email = :email"
    userdb = mysql.query_db(result,data)
    # print userdb[0]['password'], "line 116"
    print request.form['pw'], "line 117"
    # print request.form['pw'], "line 118"
    if request.form['pw'] == "":
        print "line 120"
        return redirect('/')
        flash ('no password!')
    if request.form['email'] == "":
        return redirect('/')
        flash ('no email!')
    if userdb[0]['email'] == request.form['email']:
        pass
        if userdb[0]['password'] == request.form['pw']:
            print userdb[0]['password']
            print "line 129"
            session['email'] = userdb[0]['email']
            session['firstName'] = userdb[0]['firstName']
            session['lastName'] = userdb[0]['lastName']
            session['screenName'] = userdb[0]['screenName']
            return render_template("/sucsess.html")
    if userdb[0]['email'] != request.form['email']:
        print 'line 137'
        flash('wrong password!')
        attemps += 1
        print attemps
        return redirect('/')
    if userdb[0]['password'] != request.form['pw']:
        print 'line 137'
        flash('wrong password!')
        attemps += 1
        print attemps
        return redirect('/')
    print 'poop'

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

@app.route('/lockout')
def lockout():
    render_template("/lockout.html")
    return render_template("/sucsess.html")

app.run(debug=True)
