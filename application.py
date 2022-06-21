from flask import Flask, redirect, url_for, request, render_template, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message
from dotenv import load_dotenv
from validate_email import validate_email
import os
from flask_mysqldb import MySQL
import pymysql #mysql+pymysql for sqlalchemy to connect to aws


load_dotenv()

application = Flask(__name__)
admin = Admin(application)


# DATABASE Configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{master username}:{db password}@{endpoint}/{db instance name}'
#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
#application.config['SQLALCHEMY_BINDS'] = {'about' : 'sqlite:///about.db'}
#application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# application.config['MYSQL_HOST'] = ''
# application.config['MYSQL_USER'] = ''
# application.config['MYSQL_PASSWORD'] = ''
# application.config['MYSQL_DB'] = ''

# application.config['SECRET_KEY'] = "mysecretkeywhichissupposedtobesecret" # in progress

application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("aws_rds")
application.config['SQLALCHEMY_BINDS'] = {'about' : os.getenv("aws_rds")}
application.config['SECRET_KEY'] = "mysecretkeywhichissupposedtobesecret"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)


application.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
application.config['MAIL_PORT'] = 587
application.config['MAIL_USE_TLS'] = True   
application.config['MAIL_USE_SSL'] = False  
application.config['MAIL_USERNAME'] = os.getenv("mail_user_name")
application.config['MAIL_PASSWORD'] = os.getenv("mail_user_password")
mail = Mail(application)



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

class About(db.Model):
    __bind_key__ = 'about'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


admin.add_view(SecureModelView(Project, db.session))
admin.add_view(SecureModelView(About, db.session))

# login to get access to ADMIN functionalities 
@application.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        if request.form.get("username") == os.getenv("admin_page_login") and request.form.get("password") == os.getenv("admin_page_password"):
            session["logged_in"] = True
            return redirect('admin')
        else:
            return render_template("login.html", failed=True)

    return render_template("login.html")

@application.route('/logout')
def logout():
    session.clear()
    return redirect("login")



# user accessible routes 
@application.route("/")
def index():
    return render_template("index.html")

@application.route("/projects")
def projects():

    posts = Project.query.order_by(Project.date_posted.desc()).all()

    return render_template("projects.html", posts=posts)

@application.route('/projects/<int:post_id>')
def post(post_id):
    
    post = Project.query.filter_by(id=post_id).one()

    return render_template('content.html', post=post)


@application.route('/addproject', methods=['POST'])
def addproject():
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']

    post = Project(title=title, subtitle=subtitle, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('projects'))



@application.route("/about")
def about():

    post_about = About.query.all()

    return render_template("about.html", post_about=post_about)

@application.route("/aboutedit")
def aboutedit():
    return render_template("about.html")

# contact form with handling sending emails (obviously)
@application.route("/contact")
def contact():
    return render_template("contact.html")

@application.route("/contactsent", methods=['GET','POST'])
def contact_sent():


    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # validates email addresses 
        is_valid = validate_email(f'{email}')
        if not is_valid: 
            return render_template("contact.html", fail=True)


        msg = Message(subject=f"Message from {name}, email: {email}", sender=os.getenv("mail_user_name") , recipients=["matbuziak@gmail.com"])

        msg.html = f"<h1 style='margin-left:20px'>{message}</h1>" #tbc

        mail.send(msg)
        return render_template("contact.html",success=True)


# 403 error handler after trying to access admin page without loging in
@application.errorhandler(403)
def access_forbidden(e):
    return redirect("/logout", code=302)

# 404 error after placing different combination of numbers and/or letters after "/"
@application.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == "__main__":

    application.run()
