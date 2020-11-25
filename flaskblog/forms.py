from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, College, Course, Branch, User_preference, Admin
from flaskblog import db, app,login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    firstname = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone Number',
                           validators=[DataRequired(), Length(10)])
    roll = StringField('Roll Number',
                           validators=[DataRequired(), Length(10)])
    rank = StringField('Rank',
                           validators=[DataRequired(), Length(min=1, max=20)])
    
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # def validate_firstname(self, firstname):
    #     user = User.query.filter_by(firstname=firstname.data).first()
    #     if user:
    #         raise ValidationError('That firstname is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone number is taken. Please choose a different one.')
    def validate_rank(self, rank):
        user = User.query.filter_by(rank=rank.data).first()
        if user:
            raise ValidationError('That rank is taken. Please choose a different one.')
    def validate_roll(self, roll):
        user = User.query.filter_by(roll=roll.data).first()
        if user:
            raise ValidationError('That roll number is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    email1 = StringField('Email',
                        validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    remember1 = BooleanField('Remember Me')
    submit1 = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    firstname = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone Number',
                           validators=[DataRequired(), Length(10)])
    roll = StringField('Roll Number',
                           validators=[DataRequired(), Length(10)])
    rank = StringField('Rank',
                           validators=[DataRequired(), Length(min=1, max=20)])
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # def validate_firstname(self, firstname):
    #     if firstname.data != current_user.firstname:
    #         user = User.query.filter_by(firstname=firstname.data).first()
    #         if user:
    #             raise ValidationError('That firstname is taken. Please choose a different one.')

    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class CollegeForm(FlaskForm):
    collegename = StringField('College Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add')


    def validate_collegename(self, collegename):
        college = College.query.filter_by(college_name=collegename.data).first()
        if college:
            raise ValidationError('That College is Already Present In The Database. Please choose a different one.')


class BranchForm(FlaskForm):
    branchname = StringField('Branch Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add')

    def validate_branchname(self, branchname):
        branch = Branch.query.filter_by(branch_name=branchname.data).first()
        if branch :
            raise ValidationError('That Branch is Already Present In The Database. Please choose a different one.')


class CourseForm(FlaskForm):
    collegename = StringField('College Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    branchname = StringField('Branch Name',
                           validators=[DataRequired(), Length(min=2, max=100)])

    seats = StringField('Number of Seats',
                           validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add')

    # def validate_collegename(self, collegename):
    #     college = College.query.filter_by(college_name=collegename.data).first()
    #     if college is None:
    #         raise ValidationError('That College is Not Present In The Database. Please choose a different one.')
    # def validate_branchname(self, branchname):
    #     branch = Branch.query.filter_by(branch_name=branchname.data).first()
    #     if branch is None:
    #         raise ValidationError('That Branch is Not Present In The Database. Please choose a different one.')



class PostForm(FlaskForm):
    join_query = db.session.query(College,Course,Branch)\
                    .join(Course,Course.college_id == College.college_id)\
                    .join(Branch,Branch.branch_id == Course.branch_id)
    list = []
    # list.append('hello')
    for query in join_query.all():
        s = ''
        for item in query:
            if hasattr(item,'course_id'):
                s = s + str(item.course_id)
                s = s + ' : ' 
        for item in query:
            if hasattr(item,'college_name'):
                s = s + item.college_name
                s = s + ' , '
        for item in query:
            if hasattr(item,'branch_name'):
                s = s + item.branch_name

        list.append(s)

    list1 = []
    for i in range(0,10):
        list1.append(i+1)
    title1 = SelectField('Preference Rank', validators=[DataRequired()],choices = list1)
    
    title2 = SelectField('Choices', validators=[DataRequired()],choices = list)
    submit = SubmitField('Add')

class DeclareResultForm(FlaskForm):
    submit = SubmitField('Result')


class SearchSeatForm(FlaskForm):
    collegename = StringField('College Name')
    branchname = StringField('Branch Name')
    search = SubmitField('Search')

