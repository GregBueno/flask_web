import os
from importlib import import_module
from flask import Flask, render_template, url_for, redirect, flash
from form import RegistrationForm, LoginForm

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")
@app.route("/home")
def hello():
    return "Welcome to LetMeIn!"

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'ADMIN' and form.password.data == '123':
            flash('You have been logged in!','sucess')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful','danger')
    
    return render_template('login.html',title='Login', form=form)

def create_app(env):
    module = import_module('appConf')
    EnvConfig = getattr(module, env)

    app.config.from_object(EnvConfig)
    print(" * Running on {} enviroment".format(EnvConfig.__name__))
    return app

if __name__ == "__main__":
    app = create_app("Development")
    app.run(host= '0.0.0.0', port=9195, threaded=True)