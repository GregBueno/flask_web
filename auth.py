from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Room, LogAccess, Role, Hours
from . import db
from datetime import datetime
from flask_user import roles_required, UserManager

# from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

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
    role_list = ['admin','professor','aluno']
    return render_template('signup.html',role_list=role_list)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    num_un_p = request.form.get('num_un_p')
    access_p = request.form.get('access_p')
    dt_start = request.form.get('dt_start')
    dt_end = request.form.get('dt_end')
    role_p = request.form.get('role_p')

    if access_p == 'ON':
        access_p = 1
    else:
        access_p = 0

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email,
                    password=generate_password_hash(password, method='sha256'),
                    name = name,
                    num_university = num_un_p,
                    access_permission=access_p,
                    dt_start_access = dt_start,
                    dt_end_access = dt_end)


    new_user.roles.append(Role(name=role_p))

    print(new_user)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/users')
# @roles_required('admin')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@auth.route('/rooms')
@login_required
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@auth.route('/rooms', methods=['POST'])
def rooms_post():
    room = request.form.get('room')

# ---------------------- Cad Horario

@auth.route('/hour')
def hours():
    hours = Hours.query.all()
    for i in hours:
        print(i.desc_hour)
    return render_template('hour.html')
    # , hours=hours)

@auth.route('/hour', methods=['POST'])
def hours_post():

    hour_start = request.form.get('hour_start')
    hour_end = request.form.get('hour_end')
    desc_hour = request.form.get('desc_hour')


    new_hours = Hours(hour_start = hour_start,
                    hour_end = hour_end,
                    desc_hour = desc_hour)

    print(new_hours)
    db.session.add(new_hours)
    db.session.commit()

    return render_template('hour.html', hours=hours)


# --------------------- END



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