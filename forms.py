from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UserNameForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')
