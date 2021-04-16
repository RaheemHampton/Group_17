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

@app.route('event/<event_id>/rsvp', methods=['POST'])
def rsvp(event_id):
    if session.get('user'):
        #RSVP entry is created with the user's ID and event ID
        new_rsvp = RSVP(session['user_id'], event_id)
        db.session.commit(new_rsvp)

        #Retrieve event information to be displayed on RSVP page
        event = db.session.query(Event).filter_by(id=event_id).one()
        event_creator = db.session.query(User.firstName).filterby(event.UserID)
        event_time = event.dateTime #TODO (get time from event_datetime)
        event_date = event.dateTime #TODO (get d/m/y from event_datetime)

        return render_template("rsvp.html", event_name=event.eventName,
                                            event_time=event_time,
                                            event_date=event_date,
                                            event_creator=event_creator,
                                            user=session['user'])

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.