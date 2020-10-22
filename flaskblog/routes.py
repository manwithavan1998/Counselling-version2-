import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post, College, Course, Branch, User_preference
from flask_login import login_user, current_user, logout_user, login_required
import logging

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


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
        
        


    return render_template('colleges.html', title='collegelist' , courses = courses,join_query = list)



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

        course_id1 = []
        course_id1.append(form.title1.data.split(':'))
        course_id1.append(form.title2.data.split(':'))
        course_id1.append(form.title3.data.split(':'))
        course_id1.append(form.title4.data.split(':'))
        course_id1.append(form.title5.data.split(':'))

        app.logger.info('course_id1')
        app.logger.info(form.title1.data) 
        
        for i in range(0,5):
            pref = User_preference(user_id = current_user.id,course_id = course_id1[i][0],preference_rank = i+1)
            db.session.add(pref)
            db.session.commit()
        # post = Post(title=form.title1.data, content=form.content.data, author=current_user)
        # db.session.add(post)
        # db.session.commit()
        flash('Your choices has been posted!', 'success')
        return redirect(url_for('home'))
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
        
    return render_template('choices.html', title='New Post',
                           form=form, legend='Choice Filling')


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
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


