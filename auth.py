from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Room, LogAccess
from . import db
from datetime import datetime
# import RPi.GPIO as GPIO

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email,
                    name=name,
                    password=generate_password_hash(password, method='sha256'),
                    admin=0,
                    access_permission=0)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@auth.route('/rooms')
@login_required
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@auth.route('/logaccess')
@login_required
def logaccess():
    logaccess = LogAccess.query.all()
    print(logaccess)
    return render_template('logaccess.html', logaccess=logaccess)

@auth.route('/access',methods=['POST','GET'])
@login_required
def access():
    rooms = Room.query.all()
    if request.method == 'POST':
        room_post = request.form.get('rooms')

        date_hour_now = datetime.now()
        date_hour_str = date_hour_now.strftime('%d/%m/%Y %H:%M:%S')

        print(room_post,session["user_id"],date_hour_str)

        new_log = LogAccess(room_id = room_post,
                            user_id = session["user_id"],
                            date_access = date_hour_str)

        db.session.add(new_log)
        db.session.commit()

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(LED_PIN, GPIO.OUT)
        # GPIO.output(LED_PIN, 1)
        # time.sleep(3)
        # GPIO.output(LED_PIN, 0)

    return render_template('access.html', rooms=rooms)