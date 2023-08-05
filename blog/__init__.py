from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv(".env")

# App
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
db.init_app(app)



from blog import routes
