from flask import render_template, url_for, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import utils
from app import db
from app.forms import LoginForm, RegistrationForm, ApplicationForm, GroupJoinForm, GroupRegistrationForm
from app.models import User, Application, Group

# Website Landing Page
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# Register a new User
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

# User Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)

# Administrator Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create a group for the user
@app.route("/group/create", methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupRegistrationForm()
    if form.validate_on_submit():
        group = Group(
                group_name=form.group_name.data,
                owner_id=current_user.id
                )
        group.set_password(form.password.data)
        db.session.add(group)
        # add the current user to the group
        current_user.group = group
        db.session.commit()
        return redirect(url_for('group'))
    return render_template("group_register.html", form=form)

# Allows a user to join an existing group
@app.route("/group/join", methods=['GET', 'POST'])
@login_required
def join_group():
    form = GroupJoinForm()
    if form.validate_on_submit():
        # if the current user already has an app, override it
        current_user.group = Group.query.filter_by(group_name=form.group_name.data).first()
        db.session.commit()
        return redirect(url_for('group'))
    return render_template("group_login.html", form=form)

# Get a user's currently managed group
@app.route("/group", methods=['GET'])
@login_required
def group():
    if current_user.group is None:
        return redirect(url_for('join_group'))
    return render_template("group.html")

# create a new application
@app.route("/group/application/create", methods=['GET', 'POST'])
@login_required
def create_application():
    if not current_user.is_owner():
        flash("You are not the owner of the group")
        return redirect(url_for("index"))
    form = ApplicationForm()
    if form.validate_on_submit():
        # if the current user already has an app, override it
        app = Application(
                num_apps=form.num_apps.data,
                reviews_per_app=form.reviews_per_app.data,
                semester=form.semester.data,
                group=current_user.group
                )
        current_user.get_group().application = app
        db.session.add(app)
        db.session.commit()
        return redirect(url_for('group'))
    return render_template("create_application.html", form=form)

# generate the queue and allow reviewing
@app.route("/group/application/generate", methods=['GET'])
@login_required
def generate_queue():
    if not current_user.is_owner():
        flash("You are not the owner of the group")
        return redirect(url_for("index"))
    queue = utils.generate_queue_from_application(current_user.get_application())
    current_user.get_application().application_list = utils.serialize(queue)
    db.session.commit()
    flash("Application is now open for Review")
    return redirect(url_for('index'))

@app.route("/group/application/review", methods=['GET'])
@login_required
def review_application():
    if current_user.get_application() is None or not current_user.get_application().is_active():
        flash("No open applications for your group.")
        return redirect(url_for("index"))
    app_number = utils.get_next_application(current_user)
    if app_number is None:
        flash("No more applications to review")
        return redirect(url_for("index"))
    db.session.commit()
    return render_template("review.html", application_number=app_number)

@app.route("/group/application/back", methods=['GET'])
@login_required
def put_back():
    utils.put_application_back(current_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/group/application/queue", methods=['GET'])
@login_required
def application_queue():
    q = current_user.get_application().get_application_queue()
    return render_template("queue.html", queue=q)
