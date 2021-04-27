# FLASK Project --Bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request, redirect, url_for
from database import db
from models import User as User
from models import RSVP as RSVP
from models import Event as Event
from flask import session
from flask import flash
from forms import CreateEventForm, RegisterForm, LoginForm, EditProForm
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.utils import secure_filename
from datetime import datetime
import bcrypt
import os
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
            return redirect(url_for('home', user=session['user']))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

@app.route('/signout')
def signout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('login'))

app.config['UPLOADED_IMAGES_DEST'] = "static/images"
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

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

        if form.image.data.filename != '':
            user_img = images.save(form.image.data)
        else:
            user_img='Default.jpg'
        # create user model
        new_user = User(request.form['email'], first_name, last_name, h_password, user_img)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('home'))
    else:
        # something went wrong - display register view
        return render_template('register.html', form=form)


# TODO
@app.route('/')
def home():
    # check if a user is saved in session
    if session.get('user'):
        #user_rsvps = db.session.query(Event.id).filter_by(Event.user_id == session['user_id'])
        table = db.session.query(Event, User, RSVP).join(Event, Event.user_id==User.id).outerjoin(RSVP, Event.id == RSVP.event_id and RSVP.user_id == session['user_id']).all()
        #Gets events where current user has RSVP'd to
        return render_template("home.html", user=session['user'], current_user=session['user_id'], table=table)
    else:
        return redirect(url_for('login'))

@app.route('/event/<event_id>/rsvp', methods=['POST', 'GET'])
def rsvp(event_id):
    if session.get('user'):
        if request.method == 'POST':
            new_rsvp = RSVP(session['user_id'], event_id)
            db.session.add(new_rsvp)
            db.session.commit()
            return redirect(url_for('view_event', rsvp_exists=True, event_id=event_id, user=session['user']))
        else:
            return redirect(url_for('view_event', event_id=event_id, rsvp_exists=True, user=session['user']))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/event/<event_id>/cancel-rsvp', methods=['POST', 'GET'])
def cancel_rsvp(event_id):
    if session.get('user'):
        if request.method == 'POST':
            my_rsvp = db.session.query(RSVP).filter_by(user_id = session['user_id'], event_id=event_id).one()
            db.session.delete(my_rsvp)
            db.session.commit()
            return redirect(url_for('view_event', rsvp_exists=False, event_id=event_id, user=session['user']))
        else:
            return redirect(url_for('view_event', event_id=event_id, rsvp_exists=False, user=session['user']))
    else:
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

            # If no date/time errors, create datetime object & commit all to database
            if (date_error == False) and (time_error == False):
                # combine date and time fields to create dateTime object
                date_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

                #storing event info (including newly created datetime object) in database
                new_record = Event(session['user_id'], event_name, date_time, location, description)
                db.session.add(new_record)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                return render_template('create-event.html', form=form, time_error=time_error, date_error=date_error, user=session['user'])
        else:
            # something went wrong - display register view
            return render_template('create-event.html', user=session['user'], form=form)
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/event/<event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    if session.get('user'):
        user_id = db.session.query(Event.user_id).filter_by(id=event_id).one()[0]
        if user_id == session['user_id']:
            form = CreateEventForm()
            date_error = False
            time_error = False

            if  form.validate_on_submit():
                event_name = request.form['eventname']

                date = request.form['event_date']
                if date == '': #throw error if date field is empty
                    date_error = ('Please enter a date')

                time = request.form['event_time']
                if time == '': #throw error if time field is empty
                    time_error = 'Please enter a time'

                location = request.form['location']

                description = request.form['description']

                # If no date/time errors, create datetime object & commit all to database
                updated_event = db.session.query(Event).get(event_id)
                if (date_error == False) and (time_error == False):
                    # combine date and time fields to create dateTime object
                    date_time = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

                    #storing edited event info (including edited created datetime object) in database
                    updated_event.eventName = event_name
                    updated_event.dateTime = date_time
                    updated_event.location = location
                    updated_event.description = description
                    db.session.add(updated_event)
                    db.session.commit()
                    return redirect(url_for('view_event', event_id=event_id))
                else:
                    return render_template('create-event.html', form=form, event=updated_event, time_error=time_error, date_error=date_error, user=session['user'])

            else:
                #Get request - show new note form to edit note
                #retreive event from database
                my_event = db.session.query(Event).filter_by(id=event_id).one()
                form.eventname.data = my_event.eventName
                form.location.data = my_event.location
                form.description.data = my_event.description
                date = my_event.dateTime.strftime('%Y-%m-%d')
                time = my_event.dateTime.strftime('%H:%M')

                return render_template('create-event.html', form=form, event=my_event, time=str(time), date=str(date), time_error=time_error, date_error=date_error, user=session['user'])
        else:
            return redirect(url_for('view_event', event_id=event_id))
    else:
        # user is not in session redirect to login
        return redirect(url_for('login'))

@app.route('/event/<event_id>/delete', methods=['POST'])
def delete_event(event_id):
    if session.get('user'):
        #retrieve note from database
        my_event= db.session.query(Event).filter_by(id=event_id).one()
        db.session.delete(my_event)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/event/<event_id>')
def view_event(event_id):
    if session.get('user'):
        #retrieve events from database
        rsvpExists = db.session.query(RSVP.id).filter_by(user_id=session['user_id'], event_id=event_id).first() is not None
        event = db.session.query(Event).filter_by(id = event_id).one()
        event_organizer = db.session.query(User.firstName).filter_by(id=event.user_id).one()[0]
        return render_template('event.html', event=event, event_organizer=event_organizer, rsvpExists=rsvpExists, current_user_id = session['user_id'], user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/profile/<user_id>')
def view_profile(user_id):
    if session.get('user'):

        user = db.session.query(User).filter_by(id = user_id).one()
        user_id = user.id
        first = user.firstName
        last = user.lastName
        email = user.email
        image = user.image
        table = db.session.query(Event).filter_by(user_id=user_id)
        table2 = db.session.query(Event, User, RSVP).join(Event, Event.user_id==User.id).outerjoin(RSVP, Event.id == RSVP.event_id and RSVP.user_id == session['user_id'])
        return render_template('profile.html', user=session['user'], current_user=session['user_id'],  user_first=first, user_last=last, user_email=email, 
        user_image=image, table=table, table2=table2, user_id=user_id)

    else:
        return redirect(url_for('login'))

app.config['UPLOADED_IMAGES_DEST'] = "static/images"
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

@app.route('/profile/<user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    if session.get('user'):
        if int(user_id) == int(session['user_id']):
            form = EditProForm(user_id=user_id)
            if form.validate_on_submit():

                email_errors = []
                in_email = request.form['email']
                email_in_use = (db.session.query(User).filter_by(email=in_email).count() != 0) == True and (db.session.query(User.email).filter_by(id=user_id).one()[0] == in_email) == False
                email_correct = re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', in_email) is not None

                if email_correct == False:
                    email_errors.append('Please enter a valid email')
                    my_profile = db.session.query(User).filter_by(id=user_id).one()
                    form.firstname.data = my_profile.firstName
                    form.lastname.data = my_profile.lastName
                    return render_template('register.html', form=form, profile=my_profile, email_errors=email_errors)

                if email_in_use == True:
                    email_errors.append('Email is already in use')
                    my_profile = db.session.query(User).filter_by(id=user_id).one()
                    form.firstname.data = my_profile.firstName
                    form.lastname.data = my_profile.lastName
                    return render_template('register.html', form=form, profile=my_profile, email_errors=email_errors)


                updated_profile = db.session.query(User).get(user_id)
                # salt and hash password
                h_password = bcrypt.hashpw(
                    request.form['password'].encode('utf-8'), bcrypt.gensalt())
                updated_profile.password = h_password

                # get entered user data
                first_name = request.form['firstname']
                updated_profile.firstName = first_name

                last_name = request.form['lastname']
                updated_profile.lastName = last_name

                #email retrieved from above
                updated_profile.email = in_email

                if form.image.data.filename != '':
                    user_img = images.save(form.image.data)
                    updated_profile.image = user_img

                db.session.add(updated_profile)
                db.session.commit()

                return redirect(url_for('view_profile', user_id=user_id))

            else:
                # Get request - show new register form to edit profile
                # retreive event from database
                my_profile = db.session.query(User).filter_by(id=user_id).one()
                form.firstname.data = my_profile.firstName
                form.lastname.data = my_profile.lastName
                return render_template('register.html', form=form, profile=my_profile, email_errors=[])
        else:
            return redirect(url_for('view_profile', user_id=user_id))
    else:
        return redirect(url_for('login'))


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.