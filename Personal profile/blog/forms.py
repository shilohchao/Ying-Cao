from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField,IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Regexp
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^[?=.*\d]{6,8}$',
                                                                          message='Your username should be between 6 '
                                                                                  'and 8 characters long, '
                                                                                  'and can only contain lowercase '
                                                                                  'letters.'),
                                                   EqualTo('confirm_username',
                                                           message='Usernames do not match. Try again')])
    # confirm_username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()], )
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^[?=.*\d]{6,8}$',
                                                                            message='Your password should be between 6 '
                                                                                    'and 8 characters long, '
                                                                                    'and can only contain lowercase '
                                                                                    'letters.'),
                                                     EqualTo('confirm_password',
                                                             message='Password do not match. Try again')])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exist. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    # # email = StringField('Email', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exist. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    text = TextAreaField('comment', validators=[DataRequired()])
    rate = StringField('Login', validators=[DataRequired()])
    submit = SubmitField('Comment')


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content of post')
    submit = SubmitField('post')
