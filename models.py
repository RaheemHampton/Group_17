from database import db

# Please update
class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))

    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100))
    firstName = db.Column("firstName", db.String(100))
    lastName = db.Column("lastName", db.String(100))
    password = db.Column("password", db.String(100))

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