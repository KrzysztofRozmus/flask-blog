from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from datetime import datetime
from flask_pagedown import PageDown


app = Flask(__name__)
app.secret_key = "sZzrKCW2CaYac7RQlU3kcrFNgDWWCjyfdVsyS26k"
current_datetime = datetime.now().replace(microsecond=0)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db.init_app(app)

bcrypt = Bcrypt(app)

pagedown = PageDown()
pagedown.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# When the user is not logged in, will be taken to the login page when trying to access the site
login_manager.login_view = "login"

# Message displays when a user wants to access the site but is not logged in
login_manager.login_message = "You have to log in first!"
login_manager.login_message_category = "danger"

admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

from blog import routes
