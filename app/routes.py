from flask import render_template, url_for, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import utils
from app import db
from app.forms import LoginForm, RegistrationForm, ApplicationForm
from app.models import User, Application

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
        # validate username and password
        if not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        #if validated, log the user in
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)

# Administrator Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Get a user's currently managed group
@app.route("/groups", methods=['GET'])
@login_required
def groups():
    group = current_user.group_name
    application = current_user.application
    return render_template("groups.html", group=group, app=application)

# Create a group for the user
@app.route("/groups/create", methods=['GET'])
@login_required
def create_group():
    group = current_user.group_name
    application = current_user.application
    return render_template("groups.html", group=group, app=application)

# Get a user's currently managed applications
@app.route("/groups/join", methods=['GET'])
@login_required
def join_group():
    group = current_user.group_name
    application = current_user.application
    return render_template("groups.html", group=group, app=application)

# create a new application
@app.route("/applications/create", methods=['GET', 'POST'])
@login_required
def create_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        # if the current user already has an app, override it
        app = Application(
                typeform_link=form.typeform_link.data,
                num_apps=form.num_apps.data,
                reviews_per_app=form.reviews_per_app.data,
                semester=form.semester.data,
                group=current_user
                )
        db.session.add(app)
        db.session.commit()
        return redirect(url_for('apps'))
    return render_template("create.html", form=form)

# generate the queue and allow reviewing
@app.route("/applications/generate", methods=['GET'])
@login_required
def generate_queue():
    queue = utils.generate_queue_from_application(current_user.application)
    current_user.application.application_queue = queue
    current_user.application.application_list_serial = utils.serialize(queue)
    db.session.commit()
    flash("Application is now open for Review")
    return redirect(url_for('index'))

@app.route("/applications/review", methods=['GET'])
@login_required
def review():
    app_number = utils.get_next_application(current_user.application)
    current_user.application_list_serial = utils.serialize(current_user.application.application_queue)
    db.session.commit()
    return render_template("review.html", number=app_number)

@app.route("/applications/queue", methods=['GET'])
@login_required
def application_queue():
    q = utils.deserialize(current_user.application.application_list_serial)
    return render_template("queue.html", queue=q)
