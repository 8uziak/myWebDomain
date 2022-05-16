from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():

    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template("projects.html", posts=posts)

@app.route('/projects/<int:post_id>')
def post(post_id):
    
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('content.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addproject', methods=['POST'])
def addproject():
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('projects'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)