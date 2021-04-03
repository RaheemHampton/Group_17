# FLASK Project --Bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request, redirect, url_for
from database import db
from models import Event as event
from models import User as User
from flask import flash


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
    return render_template('register.html')

# TODO
@app.route('/home', methods=['GET', 'POST'])
def home(a_user):
    return render_template('home.html')


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.