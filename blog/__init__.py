from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "sZzrKCW2CaYac7RQlU3kcrFNgDWWCjyfdVsyS26k"

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db.init_app(app)

bcrypt = Bcrypt(app)

from blog import routes
