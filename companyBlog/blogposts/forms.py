from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, ValidationError


class BlogPostForm(FlaskForm):
    # no empty titles or text possible
    # for date, that can be automatically taken from database created
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('BlogText', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Submit')
