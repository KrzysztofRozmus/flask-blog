from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv(".env")

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

from blog import routes
