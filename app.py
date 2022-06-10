from flask import Flask, redirect, url_for, request, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
admin = Admin(app)

# DATABASE Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysecretkeywhichissupposedtobesecret"
db = SQLAlchemy(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bsqvfgacavyfil:53967cd0e2c8dabdb84436d2cd47845446c3d9db315ea4e565621b8bcdf1d80f@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/ddakukmsu6ma2m'


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

admin.add_view(SecureModelView(Blogpost, db.session))

# login to get access to ADMIN functionalities 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        if request.form.get("username") == "a" and request.form.get("password") == "a":
            session["logged_in"] = True
            return redirect('admin')
        else:
            return render_template("login.html", failed=True)

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("login")


# ADMIN route only
# adding projects to database functionality 
@app.route('/add')
def add():
    return render_template('add.html')


# user accessible routes 
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


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)