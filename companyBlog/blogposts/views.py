from flask import Blueprint, render_template, redirect, url_for, abort, flash, request
from companyBlog.blogposts.forms import BlogPostForm
from companyBlog.models import db, BlogPosts
from flask_login import current_user, login_required

# register the blueprint
blogposts = Blueprint('blogposts', __name__)


# create a blog post
@blogposts.route('/createPost', methods=['GET', 'POST'])
@login_required
def createPost():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_1 = BlogPosts(title=form.title.data, post_text=form.text.data, author_id=current_user.id)
        db.session.add(blog_1)
        db.session.commit()
        # need to upgrade core.index --> index.html file for view
        return redirect(url_for("core.index"))
    return render_template("create_post.html", form=form)


# viewing a blogplost
# view as with blogpost id, pass it as integer
@blogposts.route('/<int:blog_post_id>')
def blogpost(blog_post_id):
    blog_1 = BlogPosts.query.get_or_404(blog_post_id)
    return render_template('blogpost_view.html',
                           post=blog_1)


# update blogpost

@blogposts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_1 = BlogPosts.query.get_or_404(blog_post_id)
    if blog_1.author != current_user:
        # forbidden no access
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_1.title = form.title.data
        blog_1.post_text = form.text.data
        db.session.add(blog_1)
        db.session.commit()
        flash('updated')
        # need to upgrade core.index --> index.html file for view
        return redirect(url_for('blogposts.blogpost', blog_post_id=blog_1.post_id))
    elif request.method == 'GET':
        form.title.data = blog_1.title
        form.text.data = blog_1.post_text
    return render_template("create_post.html", title='Update', form=form)


# delete blogpost

@blogposts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(blog_post_id):
    blog_1 = BlogPosts.query.get_or_404(blog_post_id)
    if blog_1.author != current_user:
        # forbidden no access
        abort(403)
    db.session.delete(blog_1)
    db.session.commit()
    flash('blogpost has been deleted')
    return redirect(url_for('users.user_posts', username=current_user.username))

