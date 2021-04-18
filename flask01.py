# FLASK Project --Bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request, redirect, url_for
from database import db
from models import Event as event
from models import User as User
from models import RSVP as RSVP
from models import Event as Event
from flask import session
from flask import flash
from forms import CreateEventForm
from datetime import datetime
import re


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

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():

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
                return redirect(url_for('home', a_user))
            else:
                # TODO
                # password was not correct, display error message
                error='Password is incorrect!'

        except:
            # email was not listed in the db for any user, disaply error message
            error = 'Email is not found!'
        return render_template('login.html', error=error)



    else:
        # GET request - show login form
        return render_template('login.html')

# TODO
@app.route('/register', methods=['GET', 'POST'])
def register():

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

        #once account creation is successful, go to homepage
        return render_template('home.html')


    else:
        # GET request - show registration form
        return render_template('register.html')


# TODO
@app.route('/home', methods=['GET', 'POST'])
def home(a_user):
    return render_template('home.html')

@app.route('/event/<event_id>/rsvp')
def rsvp(event_id):
    #### ----- REMOVE ONCE LOGIN/CREATE ACCOUNT IS FULLY IMPLEMENTED ----- ####
    session['user_id'] = 1
    session['user'] = 'Milan'

    #check that RSVP doesn't already exist
    entry_exists = db.session.query(RSVP.id).filter_by(user_id=session['user_id'], event_id=event_id).first() is not None
    #RSVP entry is created with the user's ID and event ID if it doesn't exist yet
    if(entry_exists == False):
        new_rsvp = RSVP(session['user_id'], event_id)
        db.session.add(new_rsvp)
        db.session.commit()

    #Retrieve event information to be displayed on RSVP page

    event = db.session.query(Event).filter_by(id=event_id).one()
    event_organizer = db.session.query(User.firstName).filter_by(id=event.user_id).one()[0]
    return render_template("rsvp.html", event=event, event_organizer=event_organizer, user=session['user'])

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():

    #### ----- REMOVE ONCE LOGIN/CREATE ACCOUNT IS FULLY IMPLEMENTED ----- ####
    session['user_id'] = 1
    session['user'] = 'Milan'

    form = CreateEventForm()

    date_error = False
    time_error = False

    if request.method == 'POST' and form.validate_on_submit():
        event_name = request.form['eventname']

        date = request.form['event_date']
        if date == '': #throw error if date field is empty
            date_error = ('Please enter a date')

        time = request.form['event_time']
        if time == '': #throw error if time field is empty
            time_error = 'Please enter a time'

        location = request.form['location']

        description = request.form['description']


        print(date + ' ' + time)

        print(date_error)
        print(time_error)

        # If no date/time errors, create datetime object & commit all to database
        if (date_error == False) and (time_error == False):
            # combine date and time fields to create dateTime object
            date_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

            #storing event info (including newly created datetime object) in database
            new_record = Event(session['user_id'], event_name, date_time, location, description)
            db.session.add(new_record)
            db.session.commit()
        return render_template('/create-event.html', form=form, time_error=time_error, date_error=date_error)
    else:
        # something went wrong - display register view
        return render_template('/create-event.html', form=form, time_error=time_error, date_error=date_error)




app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.