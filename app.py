"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app) # imported from models.py
db.create_all()


@app.route('/')
def show_home():
    """Shows list of all users in database and button for adding new user"""
    return redirect('/users')

@app.route('/users')
def show_users_list():
    """Shows list of all users in database and button for adding new user"""
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users = users)

@app.route('/users/new')
def show_add_form():
    """Shows an add form for users"""

    return render_template('users/form.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """Creates new user from submitted form data"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()


    return redirect(f'/users/{new_user.id}')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show info for a single user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id)

    return render_template('users/user.html', user = user, posts = posts)


@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    """Show the edit page for a user"""
    
    user = User.query.get_or_404(user_id)

    return render_template('users/edit.html', user=user)


@app.route('/users/<user_id>/edit', methods = ['POST'])
def save_edit(user_id):
    """Save edits form for a single user"""

    user = User.query.get_or_404(user_id)

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()


    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a single user"""
    User.query.filter_by(id = user_id).delete()

    # User.query.filter_by(first_name = user.first_name).delete()
    db.session.commit()


    return redirect('/users')



# BLOG POST ROUTES 

@app.route('/posts')
def show_all_posts():
    """Lists all posts from all users"""

    posts = Post.query.all()

    return render_template('posts/post_list.html', posts=posts)


@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    """Shows form to add a post for that user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('posts/addpost.html', user = user, tags = tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handles add post form; add post and redirect to user detail page"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
                title = request.form['post_title'],
                content = request.form['post_content'],
                user = user,
                tags_=tags)
    

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags_

    return render_template('posts/post.html', post = post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Shows form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()


    return render_template('posts/editpost.html', post = post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handles edit post form. Redirects back to post view"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['post_title']
    post.content = request.form['post_content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags_ = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes a blog post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")



# Tag Routes

@app.route('/tags')
def list_tags():
    """List all tags"""
    tags = Tag.query.all()

    return render_template('tags/tag_list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show detail about a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tags/tag.html', tag=tag, posts=posts)


@app.route('/tags/new')
def tag_form():
    """Shows a form to add a new tag"""

    return render_template('tags/add_tag.html')


@app.route('/tags/new', methods=['POST'])
def process_tag_form():
    """Process tag form, adds tag, and redirects ot tag list"""

    tag_name = request.form['tag_name']

    new_tag = Tag(name = tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')
    

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Shows edit form for a tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags/edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Deletes a tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')