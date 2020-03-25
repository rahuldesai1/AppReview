from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class AdminLoginForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Sign in")

class ApplicationForm(FlaskForm):
    typeform_link = StringField("Link to TypeForm", validators=[DataRequired()])
    reviews_per_app = IntegerField("Reviews per Application", validators=[DataRequired()])
    semester = StringField("Semester", validators=[DataRequired()])
    submit = SubmitField("Create App")
    

