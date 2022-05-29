from flask import render_template, url_for, request, redirect, flash, g, session
from blog import app, db
from blog.models import User, Post, Comment
from blog.forms import RegistrationForm, LoginForm, CommentForm, PostForm
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc


@app.route("/")
def home():
    posts = Post.query.order_by(desc(Post.date))
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About Me')



@app.route("/post/<int:post_id>", methods=['GET', 'POST']) # endpoint='<int:post_id>
def post(post_id):
    post=Post.query.get_or_404(post_id)
    form = CommentForm()
    if request.method=='POST':
        comment=Comment(content=request.form['comment'],
                            rate=request.form['rate'],
                            post_id=post_id,
                            user_id=session['user_id'])
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))
    comments=Comment.query.filter(Comment.post_id==post_id).all()
    return render_template('post.html',title=post.title,post=post,comments=comments)

# @app.route("/post/<int:current_post_id>", methods=['GET', 'POST'])
# def post(current_post_id):
#     post=Post.query.get_or_404(current_post_id)
#     form=CommentForm()
#     if form.validate_on_submit():
#         comment=Comment(content=form.content.data,
#                           rate=form.rate.data,
#                           post_id=current_post_id,
#                           user_id=session['user_id'])
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('post', current_post_id=current_post_id))
#     comments=Comment.query.filter(Comment.post_id==current_post_id).all()
#     return render_template('post/<int:current_post_id>.html', title=post.title, post=post, comments=comments, form=form)


@app.route("/post/new_post", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if request.method=='POST':
        post=Post(title=request.form['title'],
                  content = request.form['content'],
                  author_id = session['user_id']
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post')

    # if request.method=='POST':
    #     if request.method == 'POST':
    #         title = request.form['title']
    #         content=request.form['content']
    #         if not title:
    #             flash('title cannot be empty')
    #         elif not content:
    #             flash('content cannot be empty')
    #         else:
    #             db.session.add(post/new)
    #             db.session.commit()
    #             flash('saved successfully')
    #             redirect(url_for('home'))
    # return render_template('new.html', title='New Post', post=post)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        user = User(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('registered'))
    else:
        flash('Invalid username or password')
        return render_template('register.html', title='Register', form=form)


@app.route("/registered")
def registered():
    return render_template('registered.html', title='Thanks!')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            session['username']=form.username.data
            session['user_id']=user.id
            flash('You\'ve successfully logged in.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    session['username']=''
    session['user_id']=''
    flash('You\'re now logged out. Thanks for your visit!')
    return redirect(url_for('home'))
