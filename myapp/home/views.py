"""Create home blueprint  and all the views in it here.
"""

from flask import Blueprint, render_template

mod = Blueprint('home', __name__,
                template_folder='templates',
                static_foler='static')


@mod.route('/')
def home():
    return render_template('home/home.html')
