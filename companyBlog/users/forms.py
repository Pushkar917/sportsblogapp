from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_wtf.file import FileAllowed
from companyBlog.models import Users


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError(f"This email already exist : {field.data}")

    def check_username(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError(f"This Username already : {field.data}")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    pic = FileField('ProfilePicUpdate', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError("{}This email already exist :".format(field.data))

    def check_username(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError("{}This Username already : ".format(field.data))


