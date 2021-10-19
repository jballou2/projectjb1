import flask
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
# Point SQLAlchemy to your Heroku database
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
	db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'I am a secret key!'  # don't defraud my app ok?

from flask_login import UserMixin

db = SQLAlchemy(app)
