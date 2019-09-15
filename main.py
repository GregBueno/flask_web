from flask import Blueprint, render_template
from flask_login import login_required, current_user
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    logo = './static/logov2.png'
    return render_template('index.html', logo_img = logo)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)