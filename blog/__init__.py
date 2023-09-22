from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
from flask_admin import Admin
import os
from flask_ckeditor import CKEditor
from flask_mail import Mail
from itsdangerous.url_safe import URLSafeTimedSerializer

load_dotenv(".env")

# ========== App ==========
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
current_datetime = datetime.now().replace(microsecond=0)
app.config['UPLOAD_FOLDER'] = "blog/static/profile_pics"
app.config['UPLOAD_FOLDER2'] = "blog/static/post_title_pics"


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

# If a user wants to access user account settings, re-authentication is required unless the login is fresh.
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = "You need to reauthenticate to access this page"
login_manager.needs_refresh_message_category = "info"


# ========== Admin Panel ==========
admin = Admin(app, name="Admin Panel", template_mode="bootstrap4")
app.config['FLASK_ADMIN_SWATCH'] = "cerulean"


# ========== CKEditor ==========
ckeditor = CKEditor(app)


# ========== Email ==========
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)


# ========== URL Serializer ==========
serializer = URLSafeTimedSerializer(app.secret_key)


from blog import routes