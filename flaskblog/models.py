from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    roll = db.Column(db.String(20), unique=True, nullable=False)
    rank = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    #role = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"User('{self.id}','{self.firstname}','{self.lastname}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class College(db.Model):
    college_id = db.Column(db.Integer,primary_key = True)
    college_name = db.Column(db.String(100),nullable = False,unique = True)

    def __repr__(self):
        return f"Post('{self.college_id}', '{self.college_name}')"

class Course(db.Model):
    course_id = db.Column(db.Integer,primary_key = True)
    college_id = db.Column(db.Integer,db.ForeignKey('college.college_id'))
    no_of_seat = db.Column(db.Integer,nullable=False,)
    branch_id = db.Column(db.Integer,db.ForeignKey('branch.branch_id'),nullable=False)
    # colleges = db.relationship('College', backref='college', lazy=True)

    def __repr__(self):
        return f"Post('{self.college_id}', '{self.course_id}, '{self.branch_id}', '{self.no_of_seat}')"

class Branch(db.Model):
    branch_id = db.Column(db.Integer,primary_key = True)
    branch_name = db.Column(db.String(100),unique = True,nullable = False)

    def __repr__(self):
        return f"Post('{self.branch_id}', '{self.branch_name}')"

class User_preference(db.Model):
    
    id = db.Column(db.Integer,primary_key = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer,db.ForeignKey('course.course_id') , nullable = False)
    preference_rank = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Post('{self.id}','{self.user_id}', '{self.course_id}', '{self.preference_rank}')"


class Admin(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.id}','{self.firstname}','{self.lastname}', '{self.email}', '{self.phone}')"


class AllocatedSeat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    def __repr__(self):
        return f"Seat('{self.id}','{self.user_id}','{self.course_id}')"
