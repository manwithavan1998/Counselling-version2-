import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, AdminLoginForm,CollegeForm,BranchForm,CourseForm,DeclareResultForm
from flaskblog.models import User, Post, College, Course, Branch, User_preference, Admin, AllocatedSeat
from flask_login import login_user, current_user, logout_user, login_required
import logging
from functools import wraps
import datetime

adminset = set([1])

def adminlogin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if current_user.is_authenticated is False or current_user.id not in adminset:
            flash('Please Log In As Admin','danger')
            return redirect(url_for('Adminlogin'))
        return f(*args, **kwargs)
    return decorated_function
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data,lastname=form.lastname.data
                ,phone=form.phone.data,roll=form.roll.data,rank=form.rank.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.id not in adminset:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/Adminlogin", methods=['GET', 'POST'])
def Adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(email=form.email1.data).first()
        
        if admin and bcrypt.check_password_hash(admin.password, form.password1.data) and admin.id in adminset:
            login_user(admin, remember=form.remember1.data)
            next_page = request.args.get('next')
            app.logger.info(current_user.firstname)
            return redirect(next_page) if next_page else redirect(url_for('adminhome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('adminlogin.html', title='Admin Login', form=form)

@app.route("/adminhome", methods=['GET', 'POST'])
@adminlogin_required
def adminhome():    
    form1 = CollegeForm()
    form2 = BranchForm()
    form = CourseForm()
    form3 = DeclareResultForm()
    if form3.validate_on_submit():
        return redirect(url_for('DeclareResult'))
    if form.validate_on_submit():
        college = College.query.filter_by(college_name = form.collegename.data).first()
        branch = Branch.query.filter_by(branch_name = form.branchname.data).first()
        course = Course(college_id = college.college_id,branch_id = branch.branch_id,no_of_seat = form.seats.data)
        db.session.add(course)
        db.session.commit()
        flash('New Course Added successfully', 'success')
        return redirect(url_for('adminhome'))
    if form1.validate_on_submit():
        college1 = College(college_name = form1.collegename.data)
        db.session.add(college1)
        db.session.commit()
        flash('New College Added successfully', 'success')
        return redirect(url_for('adminhome'))
    if form2.validate_on_submit():
        branch = Branch(branch_name = form2.branchname.data)
        db.session.add(branch)
        db.session.commit()
        flash('New Branch Added successfully', 'success')
        return redirect(url_for('adminhome'))
    return render_template('adminhome.html',form1 = form1, form2 = form2,form = form,form3 = form3)
    
       

@app.route("/addcollege", methods=['GET', 'POST'])
@adminlogin_required
def addcollege():

    form = CollegeForm()
    if form.validate_on_submit():
        college1 = College(college_name = form.collegename.data)
        db.session.add(college1)
        db.session.commit()
        flash('New College Added successfully', 'success')
        return redirect(url_for('addcollege'))
    return render_template('newcollege.html',form = form)

@app.route("/addbranch", methods=['GET', 'POST'])
@adminlogin_required
def addbranch():
    form = BranchForm()
    if form.validate_on_submit():
        branch = Branch(branch_name = form.branchname.data)
        db.session.add(branch)
        db.session.commit()
        flash('New Branch Added successfully', 'success')
        return redirect(url_for('addcollege'))
    return render_template('newbranch.html',form = form)

@app.route("/addcourse", methods=['GET', 'POST'])
@adminlogin_required
def addcourse():
    form = CourseForm()
    if form.validate_on_submit():

        college = College.query.filter_by(college_name = form.collegename.data).first()
        if college is None:
            college = College(college_name = form.collegename.data)
            db.session.add(college)
            db.session.commit()
        branch = Branch.query.filter_by(branch_name = form.branchname.data).first()
        if branch is None:
            branch = Branch(branch_name = form.branchname.data)
            db.session.add(branch)
            db.session.commit()
        college = College.query.filter_by(college_name = form.collegename.data).first()
        branch = Branch.query.filter_by(branch_name = form.branchname.data).first()
        course = Course(college_id = college.college_id,branch_id = branch.branch_id,no_of_seat = form.seats.data)
        db.session.add(course)
        db.session.commit()
        flash('New Course Added successfully', 'success')
        return redirect(url_for('addcourse'))
    return render_template('newcourse.html',form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/seat matrix")
def seat_matrix():
    colleges = College.query.all()
    courses = Course.query.all()
    branches = Branch.query.all()
    join_query = db.session.query(College,Course,Branch)\
                    .join(Course,Course.college_id == College.college_id)\
                    .join(Branch,Branch.branch_id == Course.branch_id)
    list = []
    for query in join_query.all():
        temp = []
        for item in query:
            if hasattr(item,'college_name'):
                temp.append(item.college_name)
            if hasattr(item,'branch_name'):
                temp.append(item.branch_name)
            if hasattr(item,'no_of_seat'):
                temp.append(item.no_of_seat)
        list.append(temp)
    list.sort()
    return render_template('colleges.html', title='collegelist' , courses = courses,join_query = list)


@app.route("/adminseatmatrix")
@adminlogin_required
def adminseat_matrix():
    colleges = College.query.all()
    courses = Course.query.all()
    branches = Branch.query.all()
    join_query = db.session.query(College,Course,Branch)\
                    .join(Course,Course.college_id == College.college_id)\
                    .join(Branch,Branch.branch_id == Course.branch_id)
    list = []
    for query in join_query.all():
        temp = []
        for item in query:
            if hasattr(item,'college_name'):
                temp.append(item.college_name)
            if hasattr(item,'branch_name'):
                temp.append(item.branch_name)
            if hasattr(item,'no_of_seat'):
                temp.append(item.no_of_seat)
        list.append(temp)
    
    list.sort() 
        
    return render_template('admincolleges.html', title='collegelist' , courses = courses,join_query = list)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        if current_user.rank != form.rank.data or current_user.roll != form.roll.data:
            flash('You can not update your roll number or rank ' ,'danger')
        else:
            db.session.commit()
            flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname   
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.roll.data = current_user.roll
        form.rank.data = current_user.rank   
    

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        
        # course_id1.append(form.title1.data.split(':'))
        # course_id1.append(form.title2.data.split(':'))
        # course_id1.append(form.title3.data.split(':'))
        # course_id1.append(form.title4.data.split(':'))
        # course_id1.append(form.title5.data.split(':'))
        pref_rank = form.title1.data
        TEMP = form.title2.data.split(':')
        Course_id = TEMP[0]
        app.logger.info('course_id1')
        app.logger.info(form.title1.data) 
        User_preference.query.filter_by(user_id = current_user.id , preference_rank = pref_rank).delete()
        db.session.commit()

        pref = User_preference(user_id = current_user.id,course_id = Course_id,preference_rank = pref_rank)
        db.session.add(pref)
        db.session.commit()
        # post = Post(title=form.title1.data, content=form.content.data, author=current_user)
        # db.session.add(post)
        # db.session.commit()
        flash('Your choices has been posted!', 'success')
        return redirect(url_for('new_post'))
    # elif request.method == 'GET':
    #     exists = db.session.query(
    #             db.session.query(User_preference).filter_by(user_id = current_user.id).exists()
    #         ).scalar()
    #     if(exists == False):
    #         app.logger.info('hello')
    #     choices = User_preference.query.filter_by(user_id = current_user.id)
    #     # app.logger.info(choices[0].course_id)
        # app.logger.info(choices[1].course_id)
        # if exists :
        #     list[0] = choices[0].course_id
        #     list1 = list[:]
            
        #     form.title1.choices = list
        #     list1[0] = choices[1].course_id    
        #     form.title2.choices = list1
        #     list2 = list[:]
        #     list2[0] = choices[2].course_id
        #     form.title3.choices = list2
        #     list3 = list[:]
        #     list3[0] = choices[3].course_id
        #     form.title4.choices = list3
        #     list4 = list[:]
        #     list4[0] = choices[4].course_id
        #     form.title5.choices = list4
        # else:
        # form.title1.choices = list
        # form.title2.choices = list
        # form.title3.choices = list
        # form.title4.choices = list
        # form.title5.choices = list
    list = []
    list = User_preference.query.filter_by(user_id = current_user.id).all()
    join_query = db.session.query(College,Course,Branch)\
                    .join(Course,Course.college_id == College.college_id)\
                    .join(Branch,Branch.branch_id == Course.branch_id)
    new_list = []
    for x in list:
        temp_list = []
        temp_list.append(x.id)
        temp_list.append(x.preference_rank)
        for query in join_query.all():
            if query[1].course_id == x.course_id:
                temp_list.append(query[0].college_name)
                temp_list.append(query[2].branch_name)

            # for item in query:
            #     if hasattr(item,'college_name') and x.course_id == 3:
            #         temp_list.append(item.college_name)
            # for item in query:
            #     if hasattr(item,'branch_name') and x.course_id == 3:
            #         temp_list.append(item.branch_name)

        new_list.append(temp_list)

    new_list.sort(key = lambda new_list: new_list[1])
    app.logger.info(new_list)
    allocationList = AllocatedSeat.query.filter_by(user_id = current_user.id)
    allocatedCollege = "Unfortunately You Have Not Been Alloted Any Course."
    allocatedBranch = ""
    for x in list:

        for query in join_query.all():
            try:
                if query[1].course_id == allocationList[0].course_id:
                   allocatedCollege = query[0].college_name
                   allocatedBranch = query[2].branch_name
            except:
                allocatedCollege = "Unfortunately You Have Not Been Alloted Any Course."

            # for item in query:
            #     if hasattr(item,'college_name') and x.course_id == 3:
            #         temp_list.append(item.college_name)
            # for item in query:
            #     if hasattr(item,'branch_name') and x.course_id == 3:
            #         temp_list.append(item.branch_name)
    current_time = datetime.datetime.now() 


    return render_template('choices.html', title='New Post',
                           form=form, legend='Choice Filling',pref = new_list,
                           allocatedCollege = allocatedCollege,allocatedBranch = allocatedBranch, current_time = current_time )


# @app.route("/post/<int:post_id>")
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post.html', title=post.title, post=post)


# @app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated!', 'success')
#         return redirect(url_for('post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='Update Post',
#                            form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    app.logger.info("post_id = ")
    app.logger.info(post_id)
    post = User_preference.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('new_post'))



@app.route('/DeclareResult',methods=['GET','POST']) 
@adminlogin_required
def DeclareResult():
    db.session.query(AllocatedSeat).delete()
    db.session.commit()
    allCourse = Course.query.all()
    course = {}
    for item in allCourse:
        course[item.course_id] = item.no_of_seat

    join_query = db.session.query(User,User_preference)\
                    .join(User,User.id == User_preference.user_id)

    list = []

    for item in join_query:
        temp = []
        temp.append(item[0].rank)
        temp.append(item[1].preference_rank)
        temp.append(item[0].id)  
        temp.append(item[1].course_id)
        list.append(temp)

    list.sort()
    dict = {}
    pre_user = -1
    for item in list:
        if item[2] != pre_user and course[item[3]]>0:
            course[item[3]]-=1
            pre_user = item[2]
            dict[item[2]] = item[3]

    for item in dict:
        allocation = AllocatedSeat(user_id = item,course_id = dict[item])
        db.session.add(allocation)
        db.session.commit()

    return redirect(url_for('adminhome'))

    
