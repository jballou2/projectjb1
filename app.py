import os
import flask
from flask_sqlalchemy import SQLAlchemy



app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://zcgkyytmmrackv:c4bc1a99c5fe2c959ec72a161d9839d00c2bb0727f6569e2ebc64bdcacaa4c72@ec2-54-208-96-16.compute-1.amazonaws.com:5432/d83u6tj4mknpqu"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
db.create_all()


@app.route("/", methods = ["GET", "POST"])
def index():
    if flask.request.method == "POST":
        name = flask.request.form.get("username")

        
        task=Task(name=name)
        db.session.add(task)
        db.session.commit()
    if flask.request.method == "GET":
        items = Task.query.all()
        
        name= []
        for item in items:
            name.append(item.username)
    return flask.render_template(
        "signup.html",
        name=name
    )
app.run(use_reloader = True)
