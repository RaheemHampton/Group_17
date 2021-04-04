from database import db
from datetime import datetime

# Please update
class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    
    eventName = db.Column(db.String(150))
    dateTime = db.Column(db.DateTime(100))
    location = db.Column(db.String(100))
    description = db.Column(db.Text(500))

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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    password = db.Column(db.String(200), nullable=False)

    #1 user -> many events, 1 user -> many rsvps
    events = db.relationship('Event')
    rsvps = db.relationship('RSVP')

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
    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    EventID = db.Column(db.Integer, db.ForeignKey('Event.id'), nullable=False)


    def __init__(self, UserID, eventID):
        self.UserID = UserID
        self.EventID = eventID
