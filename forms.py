from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email, Optional
from flask_wtf.file import FileAllowed
from wtforms import ValidationError, FileField, HiddenField
from models import User
from database import db


class CreateEventForm(FlaskForm):
    class Meta:
        csrf = False

    eventname = StringField('Event Name', validators=[DataRequired(message="Must enter an event name"),
                                                      Length(max=150, message="Event name must be no longer than 150 characters")])
    #Validation for date and time are done inside create_event route
    location = StringField('Location Name', validators=[Length(0, 100, message= "Location must be no longer than 100 characters")])
    description = StringField('Description', validators=[Length(0, 500, "Description must be no longer than 100 characters")])


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1, 10)])

    lastname = StringField('Last Name', validators=[Length(1, 20)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10)
    ])

    image = FileField('Upload Image', validators=[
        Optional(), FileAllowed(['jpg', 'png'], 'Images only!')])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Email already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')

class EditProForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1, 10)])

    lastname = StringField('Last Name', validators=[Length(1, 20)])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10)
    ])

    image = FileField('Upload Image', validators=[
        Optional(), FileAllowed(['jpg', 'png'], 'Images only!')])

    submit = SubmitField('Submit')




