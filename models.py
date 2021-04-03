from database import db
from datetime import datetime

# Please update
class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column("EventID", db.Integer, primary_key=True)
    UserID = db.Column("UserID", db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    
    eventName = db.Column("eventName", db.String(150))
    dateTime = db.Column("dateTime", db.DateTime(100))
    location = db.Column("location", db.String(100))
    description = db.Column("description", db.Text(500))

    # relations
    rvsps = db.relationship('RSVP')

    def __init__(self, UserID, eventName, dateTime, location, description):
        self.UserID = UserID
        self.eventName = eventName
        self.dateTime = dateTime
        self.location = location
        self.description = description 

class User(db.Model):
    __tablename__ = "User"
    id = db.Column("UserID", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))
    firstName = db.Column("firstName", db.String(100))
    lastName = db.Column("lastName", db.String(100))
    password = db.Column("password", db.String(100), nullable=False)

    # relations
    events = db.relationship('event')
    rvsps = db.relationship('RSVP')

    def __init__(self, email, firstName, lastName, password):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.password = password

    def pwdCheck(self, password):
        if self.password == password:
            return True
        else:
            return False


class RSVP(db.Model):
    __tablename__ = "RSVP"
    id = db.Column("id", db.Integer, primary_key=True)
    UserID = db.Column("UserID", db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    EventID = db.Column("EventID", db.Integer, db.ForeignKey('Event.EventID'), nullable=False)


    def __init__(self, UserID, eventID):
        self.UserID = UserID
        self.EventID = EventID
