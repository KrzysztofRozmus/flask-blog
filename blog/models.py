from blog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=True)
    email = db.Column(db.String(30), unique=True, nullable=True)
    password = db.Column(db.String(40), nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"
