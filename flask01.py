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
from forms import CreateEventForm, RegisterForm, LoginForm
from datetime import datetime
import bcrypt
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
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.firstName
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('home'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(request.form['email'], first_name, last_name, h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('login'))
    else:
        # something went wrong - display register view
        return render_template('register.html', form=form)


# TODO
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/event/<event_id>/rsvp')
def rsvp(event_id):
    if session.get('user'):
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
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if session.get('user'):
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
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))




app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.