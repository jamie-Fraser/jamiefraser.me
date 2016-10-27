from flask_wtf import Form
from werkzeug import secure_filename
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms.validators import DataRequired, Length
from .models import User

class LoginForm(Form):
    remember_me = BooleanField('remember_me', default=False)
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email')
    password = PasswordField('password', validators=[DataRequired()])
    
class ContactForm(Form):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Length(min=0, max=80)])
    subject = StringField('subject', validators=[Length(min=0, max=140)])
    message = TextAreaField('message', validators=[DataRequired(), Length(min=0, max=2000)])
    
class PortfolioItemForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[Length(min=0, max=2000)])
    artwork_path = FileField('artwork_path', validators=[ FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!') ])
    