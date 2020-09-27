from flask import render_template, url_for, flash, request, Blueprint, redirect
from companyBlog import db, cache
from flask_login import login_user, current_user, logout_user, login_required
from companyBlog.models import Users, BlogPosts
from companyBlog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from companyBlog.users.picture_handler import *

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        newuser = Users(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# Login user
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # this step gets the user's email[must have been in database when you register] detail, from database
        loggeduser = Users.query.filter_by(email=form.email.data).first()
        if loggeduser:
            if loggeduser.checkPassword(form.password.data) and loggeduser is not None:
                # login the user if password matches of with hashed password in database
                login_user(loggeduser)
                # As protocol of flask, flask saves the user's requested url(where user wants to go), which requires log
                # in next keyword. Flask saves the keyword in next
                next = request.args.get('next')

                # checking if user wanted to go in URL which requires login
                # Hence we are checking next, has any value or not

                if next is None or not next[0] == '/':
                    next = url_for("core.index")
                return redirect(next)
        else:
            flash("Register first with mail id provided.")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


# Logout
@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("logged out succesfully")
    return redirect(url_for("users.login"))


# update the account
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.pic.data:
            username = current_user.username
            addedpic = add_profile_pic(form.pic.data, username)
            current_user.profile_image = addedpic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account updated")
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='Profile_Pic/' + current_user.profile_image)
    return render_template("account.html", form=form)


# individual users view
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPosts.query.filter_by(author=user).order_by(BlogPosts.timeofPost.desc()).paginate(page=page,
                                                                                                       per_page=8)
    next_url = url_for('users.user_posts',username=user.username, blog_posts=blog_posts,page=blog_posts.next_num) \
        if blog_posts.has_next else None
    prev_url = url_for('users.user_posts', username=user.username, blog_posts=blog_posts, page=blog_posts.next_num) \
        if blog_posts.has_prev else None
    return render_template("user_blogPost.html", blog_posts=blog_posts, user=user, next_url=next_url,
                           prev_url=prev_url)
