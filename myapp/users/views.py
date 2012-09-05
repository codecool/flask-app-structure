from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask.ext.login import login_required, login_user, logout_user, current_user
from sqlalchemy.orm import defer
from sqlalchemy.orm.exc import NoResultFound

from ..models import User
from forms import LoginForm

mod = Blueprint('users', __name__, template_folder='templates',
                       static_folder='static')

@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        try:
            user = User.query.filter(User.email == form.email).options(defer('_password')).one()
        except NoResultFound:
            flash('No such email exists.')
        else:
            if user.match_password(form.password):
                login_user(user)
                flash('You are successfully logged in.')
                return redirect(url_for('home.home'))
            else:
                flash('Wrong email/password combination. Try again!')
    if current_user.is_authenticated():
        flash('You are already logged in.')
        redirect('/')
    return render_template('users/login.html', form=form)


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))