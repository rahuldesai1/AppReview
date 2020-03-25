from flask import render_template, url_for, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import db
from app.forms import AdminLoginForm, AdminRegistrationForm
from app.models import Administrator

# Website Landing Page
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# Administrator Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        # validate username and password
        user = Administrator.query.filter_by(group_name=form.group_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        #if validated, log the user in
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template("login.html", form=form, admin=True)

# Administrator Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new Administrator/Group
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        user = Administrator(group_name=form.group_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

# create a user account
@app.route("/create", methods=['GET'])
@login_required
def create():
    return redirect(url_for('index'))

# Get a user's currently managed applications
@app.route("/apps", methods=['GET'])
@login_required
def apps():
    return redirect(url_for('index'))
