from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Room, LogAccess, Role, Hours, HourRegister
from . import db
from datetime import datetime
from flask_user import roles_required, UserManager, current_user, UserMixin
# from flask_security import Principal, Permission, RoleNeed

# from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

# import RPi.GPIO as GPIO

auth = Blueprint('auth', __name__)

@auth.route("/TestUser")
def user_role():
    # user_roles = any(role.name for role in current_user.roles if role.name in ['aluno','professor'])
    checked_role = current_user.has_role(['admin'])
    return str(checked_role)

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
    users = User.query.all()

    return render_template('signup.html',role_list=role_list,users=users)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    num_un_p = request.form.get('num_un_p')
    # access_p = request.form.get('access_p')
    dt_start = request.form.get('dt_start')
    dt_end = request.form.get('dt_end')
    role_p = request.form.get('role_p')

    access_p = 'OFF'
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

# ---------------------- Cad Room

@auth.route('/rooms')
@login_required
def rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@auth.route('/rooms', methods=['POST'])
def rooms_post():
    room = request.form.get('room')
    new_room = Room(room=room)
    db.session.add(new_room)
    db.session.commit()

    return redirect(url_for('auth.rooms'))

# --------------------- End Cad Room

# ---------------------- Cad Horario

@auth.route('/hour')
def hours():
    hours = Hours.query.all()

    return render_template('hour.html', hours=hours)

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

    return redirect(url_for('auth.hours'))

# --------------------- End Cad Horario

# ---------------------- Register Access

@auth.route('/register_access')
def register_access():

    rooms = Room.query.all()
    hours = Hours.query.all()
    users = User.query.all()

    list_access = db.session.query(HourRegister, Room, User, Hours
    ).join(Room, Room.id == HourRegister.room_id
    ).join(User, User.id == HourRegister.user_id
    ).join(Hours, Hours.id == HourRegister.hours_id
    ).filter(User.name != 'test'
    ).all()

    # for tt in list_access:
    #     print( tt[1].room,
    #            tt[2].name,
    #            tt[0].dt_access,
    #            tt[3].desc_hour,
    #            tt[0].description)

    return render_template('register_access.html', room_list=rooms, user_list=users, list_hour=hours, list_access = list_access)

@auth.route('/register_access', methods=['POST'])
def register_access_post():

    room = request.form.get('room_list')
    user = request.form.get('user_list')
    dt_access = request.form.get('dt_access')
    hour = request.form.get('hour_list')
    description = request.form.get('description')

    hours_selected = Hours.query.filter_by(id= hour).first()

    dt_start_access = dt_access + ' ' + hours_selected.hour_start
    dt_end_access = dt_access + ' ' + hours_selected.hour_end

    print(dt_start_access, dt_end_access)
    # dt_access = dt_access + ' ' + hour_access
    # date_time_access = datetime.strptime(date_access, '%d/%m/%Y %H:%M:%S')

    new_access = HourRegister(room_id = room, user_id = user, dt_access = dt_access, hours_id = hour, description = description, dt_start_access = dt_start_access, dt_end_access = dt_end_access)
    # print(room,user,dt_access,hour,description)

    db.session.add(new_access)
    db.session.commit()

    return redirect(url_for('auth.register_access'))
# --------------------- End Register Access

@auth.route('/logaccess')
@login_required
def logaccess():
    # logaccess = LogAccess.query.all()

    logaccess = db.session.query(LogAccess, Room, User
    ).join(Room, Room.id == LogAccess.room_id
    ).join(User, User.id == LogAccess.user_id
    ).all()

    print(logaccess)
    return render_template('logaccess.html', logaccess=logaccess)

# ---------------------- Access Room
@auth.route('/access',methods=['POST','GET'])
@login_required
def access():
    rooms = Room.query.all()
    if request.method == 'POST':
        room_post = request.form.get('rooms')
        dt_access = request.form.get('dt_access')
        hour_access = request.form.get('hour_access')

        date_access = dt_access + ' ' + hour_access
        date_time_access = datetime.strptime(date_access, '%d/%m/%Y %H:%M:%S')

        print(room_post, date_access)

        list_access = db.session.query(HourRegister, Room, User, Hours
        ).join(Room, Room.id == HourRegister.room_id
        ).join(User, User.id == HourRegister.user_id
        ).join(Hours, Hours.id == HourRegister.hours_id
        ).filter(Room.id == room_post, User.id == session["user_id"], HourRegister.dt_access == dt_access
        ).all()

        if len(list_access) > 0:
            flash([1,'Access released.'],category='info')

            new_log = LogAccess(room_id = room_post,
                    user_id = session["user_id"],
                    date_access = date_access)

            db.session.add(new_log)
            db.session.commit()

            # Print query
            for tt in list_access:
                print(tt[1].room,
                    tt[2].name,
                    tt[0].dt_access,
                    tt[3].hour_start,
                    tt[3].hour_end,
                    tt[0].description)


            # if  date_time_obj_in <= date_time_obj <= date_time_obj_end:
            #     print(date_time_obj)

            # Colocar aqui o RASP

            # GPIO.setmode(GPIO.BOARD)
            # GPIO.setup(LED_PIN, GPIO.OUT)
            # GPIO.output(LED_PIN, 1)
            # time.sleep(3)
            # GPIO.output(LED_PIN, 0)

        else:
            flash([0,'Access denied.'],category='info')

        # date_hour_now = datetime.now()
        # date_hour_str = date_hour_now.strftime('%d/%m/%Y %H:%M:%S')

        # print(room_post,session["user_id"],date_hour_str)


    return render_template('access.html', rooms=rooms)

# ---------------------- End Access Room