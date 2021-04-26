from database import db
from datetime import datetime

# Please update
class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    eventName = db.Column(db.String(150))
    dateTime = db.Column(db.DateTime())
    location = db.Column(db.String(100))
    description = db.Column(db.Text(500))

    # relations: 1 event has many rsvps
    rvsps = db.relationship('RSVP', backref="Event", lazy=True)

    def __init__(self, user_id, eventName, dateTime, location, description):
        self.user_id = user_id
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
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(200))

    #relations: 1 user -> many events, 1 user -> many rsvps
    events = db.relationship("Event", backref="User", lazy=True)
    rsvps = db.relationship("RSVP", backref="User", lazy=True)

    def __init__(self, email, firstName, lastName, password, image):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.image = image

    def pwdCheck(self, password):
        if self.password == password:
            return True
        else:
            return False


class RSVP(db.Model):
    __tablename__ = "RSVP"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("Event.id"), nullable=False)


    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id
