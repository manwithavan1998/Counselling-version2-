from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, College, Course, Branch, User_preference
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

    def validate_firstname(self, firstname):
        user = User.query.filter_by(firstname=firstname.data).first()
        if user:
            raise ValidationError('That firstname is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


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

    def validate_firstname(self, firstname):
        if firstname.data != current_user.firstname:
            user = User.query.filter_by(firstname=firstname.data).first()
            if user:
                raise ValidationError('That firstname is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


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
    # app.logger.info('hello')
    # app.logger.info(current_user)
    # exists = db.session.query(
    #             db.session.query(User_preference).filter_by(user_id = (current_user.id)).exists()
    #         ).scalar()
    # if(exists == False):
    #     app.logger.info('hello')
    # choices = User_preference.query.filter_by(user_id = (current_user.id))
    # app.logger.info(choices[0].course_id)
    # app.logger.info(choices[1].course_id)
    # if exists :
    #     list[0] = choices[0].course_id
    #     list1 = list[:]
    #     list1[0] = choices[1].course_id    
    #     list2 = list[:]
    #     list2[0] = choices[2].course_id 
    #     list3 = list[:]
    #     list3[0] = choices[3].course_id
    #     list4 = list[:]
    #     list4[0] = choices[4].course_id
    #     title1 = SelectField('Choice 1', validators=[DataRequired()],choices = list)
    #     title2 = SelectField('Choice 2', validators=[DataRequired()],choices = list1)
    #     title3 = SelectField('Choice 3', validators=[DataRequired()],choices = list2)
    #     title4 = SelectField('Choice 4', validators=[DataRequired()],choices = list3)
    #     title5 = SelectField('Choice 5', validators=[DataRequired()],choices = list4)
    # else:
    # title1 = SelectField('Choice 1', validators=[DataRequired()],choices = list)
    # title2 = SelectField('Choice 2', validators=[DataRequired()],choices = list)

    # title3 = SelectField('Choice 3', validators=[DataRequired()],choices = list)
    # title4 = SelectField('Choice 4', validators=[DataRequired()],choices = list)
    # title5 = SelectField('Choice 5', validators=[DataRequired()],choices = list)
    #     # content = TextAreaField('Content', validators=[DataRequired()])
    # submit = SubmitField('Post')
    list1 = []
    for i in range(0,10):
        list1.append(i+1)
    title1 = SelectField('Preference Rank', validators=[DataRequired()],choices = list1)
    
    title2 = SelectField('Choices', validators=[DataRequired()],choices = list)
    submit = SubmitField('Add')
