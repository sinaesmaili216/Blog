from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from flask import Flask, render_template, session, request, redirect, url_for
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import DateTimeField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from wtforms.widgets.core import TextArea

from werkzeug.exceptions import abort

from countries.auth import login_required
from countries.db import get_db


#app = Flask(__name__)

#app.config['SECRET_KEY'] = "DEV"
#add database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#initialize database
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)



bp = Blueprint('blog', __name__)

#show posts in first page
@bp.route("/")
def index():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template("posts.html", posts=posts)


#delete user
@bp.route("/user/<username>")
def profile(username):
    db = get_db()
    db.execute('DELETE FROM user WHERE username=(?)', (username,))
    db.commit()
    return "user deleted seccessfully!!"




@bp.route("/posts/delete/<int:id>")
def delete_post(id):
    db = get_db()
    

    db.execute('DELETE FROM posts WHERE id=(?)', (id,))
    db.commit()
    flash("The Post Was Deleted!!")

    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template("posts.html", posts=posts)

    


#creat user form
class UserForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField("password2", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create post form
class PostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    date_created = DateTimeField("date_created", validators=[DataRequired()], default=datetime.now())
    username = StringField("username", validators=[DataRequired()])
    submite = SubmitField("Submite")

#add post page
@bp.route('/add-post', methods=["GET","POST"])
def add_post():
    db = get_db()
    form = PostForm()
    if form.validate_on_submit():
        db.execute('INSERT INTO posts (title, content, author, date_created)\
            VALUES (?,?,?,?)', (form.title.data, form.content.data, form.author.data, form.date_created.data))
        #Posts(title=form.title.data, content=form.content.data, author=form.author.data)
       
        #clear the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''

        #add post to database
        db.commit()
        
        flash("post submited seccessfully")

    #redirect to web page
    return render_template("add_post.html", form=form)





#create users model
#class Users(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(200), nullable=False)
#    email = db.Column(db.String(200), nullable=False, unique=True)
#    date_added = db.Column(db.DateTime, default=datetime.now)

#    def __repr__(self):
 #       return f"name: {self.name}"

@bp.route("/user/add", methods=["GET", "POST"])
def add_user():
    db = get_db()
    name = None
    
    form = UserForm()
    if form.validate_on_submit():
        #user = db.execute('SELECT * FROM user WHERE email=(?)',(form.email.data))
        #Users.query.filter_by(email= form.email.data).first()
      
     
        #if user in None:
        db.execute('INSERT INTO user (username, email, password) VALUES (?,?,?)',(form.name.data, form.email.data, form.password.data))
            #Users(name=form.name.data, email=form.email.data)
            
        db.commit()
        
        name= form.name.data
        #clear form
        form.name.data = ''
        form.email.data = ''
        form.password.data = ''
        flash("user added successfuly")
    
    return render_template("add_user.html", form=form, name=name)


#show all users
@bp.route("/users")
def users_list():
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()

    return render_template("users_list.html", users=users)


@bp.route("/profile/<username>")
def user_profile(username):
    db = get_db()
    user_posts = db.execute('SELECT * FROM posts WHERE username=(?)', (username,))

    return render_template("profile.html", user_posts=user_posts)