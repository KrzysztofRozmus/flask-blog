from flask import Flask


app = Flask(__name__)
app.secret_key = "sZzrKCW2CaYac7RQlU3kcrFNgDWWCjyfdVsyS26k"


from blog import routes