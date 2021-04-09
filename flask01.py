# FLASK Project --Bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request, redirect, url_for
from database import db
from models import Event as Event
from models import User as User
from flask import flash
import re
import datetime


app = Flask(__name__)     # create an app
app.secret_key = "super secret key"

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_event_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)

# Setup models
with app.app_context():
    db.create_all()   # run under the app context

# global variable to hold currently logged in account, make sure to reset for logout
currentAcc = None


@app.route('/login', methods=['GET', 'POST'])
def login():
    global currentAcc
    error = None
    # check method used for request
    if request.method == 'POST':
        # get email data
        in_email = request.form['email']
        # get password data
        in_password = request.form['password']

        # create date stamp
        from datetime import date
        today = date.today()
        today = today.strftime("%m-%d-%Y")

        # retrieve user from database
        try:
            a_user = db.session.query(User).filter_by(email=in_email).one()
            
            # check if was correct password
            if a_user.pwdCheck(in_password):
                # password was correct, redirect to home page for user
                flash('Successful login')
                currentAcc = a_user
                print(currentAcc != None)
                return redirect(url_for('home'))
            else:
                # password was not correct, display error message
                error='Password is incorrect!'

        except Exception as e:
            # email was not listed in the db for any user, disaply error message
            error = 'Email is not found!'
            print(e)
        return render_template('login.html', error=error)



    else:
        # GET request - show login form
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    global currentAcc
    error = None

    if request.method == 'POST':
        #get first name
        first_name = request.form['first_name']
        #get last name
        last_name = request.form['last_name']
        # get email data
        in_email = request.form['email']
        # get password data
        password = request.form['password']

        #checks if email is in a proper format
        email_correct = re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', in_email) is not None

        if email_correct == False:
            error = 'Please enter a valid email address '
            return render_template('register.html', error=error)

        # searches database to see if email has been used
        user_exists = db.session.query(User.id).filter_by(email = in_email).first() is not None

        if user_exists == True:
            error = 'An email for this account has already been registered'
            return render_template('register.html', error=error)

        print(first_name, last_name, in_email, user_exists, 'Email correct: ', email_correct, 'User exists: ', user_exists)

        new_record = User(in_email, first_name, last_name, password)
        db.session.add(new_record)
        db.session.commit()

        currentAcc = a_user

        #once account creation is successful, go to homepage
        return redirect(url_for('home', a_user=currentAcc))


    else:
        # GET request - show registration form
        return render_template('register.html')


# TODO
@app.route('/home', methods=['GET', 'POST'])
def home():
    global currentAcc
    if (currentAcc != None):
        error = None
        return render_template('home.html', a_user=currentAcc)
    else:
        currentAcc = None
        return redirect(url_for('login'))


@app.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    global currentAcc
    print(currentAcc)
    if (currentAcc != None):
        error = None
        # check method used for request
        if request.method == 'POST':
            # get event name
            event_name = request.form['event_name']
            # get event date
            event_date = request.form['event_date']
            # get event time
            # tzinfo attribute needs to be kept for time
            event_time = request.form['event_time']
            # get event location
            event_location = request.form['event_location']
            # get event description
            description = request.form['description']
            # get event image
            # TODO

            # TODO Parse date and time form inputs into date and time datetime
                # objects?

            # create date stamp from date and time
            event_datetime = datetime.datetime.combine(event_date, event_time)


            try:
                UserID, eventName, dateTime, location, description
                new_event = Event(currentAcc.id, event_name, event_datetime, event_location, description)
                db.session.add(new_event)
                db.session.commit()

                #once event creation is successful, go back to homepage
                return redirect(url_for('home', a_user=currentAcc))

            except Exception as e:
                # event creation failed
                error = str(e)
                print(e)
                # send flash message
                flash(error)

        else:
            # GET request - show createEvent form
            return render_template('createEvent.html', a_user=currentAcc)

    else:
        currentAcc = None
        return redirect(url_for('login'))


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)), debug=True)


# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.