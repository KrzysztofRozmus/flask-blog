from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from flask_admin import Admin
import os


load_dotenv(".env")

current_datetime = datetime.now().replace(microsecond=0)

# ========== App ==========
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ========== Database ==========
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db.init_app(app)

# ========== User authentication ==========
login_manager = LoginManager()
login_manager.init_app(app)
# If user wants to access login_required page without being logged in, will be redirect to login page.
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

app.config['UPLOAD_FOLDER'] = "blog/static/profile_pics"

# ========== Admin Panel ==========
admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")
app.config['FLASK_ADMIN_SWATCH'] = "cerulean"

from blog import routes