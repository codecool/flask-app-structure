from flask.ext.wtf import Form, TextField, PasswordField, SubmitField
from wtforms.validators import Required, Length


class LoginForm(Form):
    email = TextField(u'Email', validators=[Required()])
    password = PasswordField(u'Password', validators=[Required(), Length(min=5)])
    submit = SubmitField(u'Submit')