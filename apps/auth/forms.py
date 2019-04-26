from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField(u'用户', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField(u'登录')

