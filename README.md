# Flask Web Application

Web application develop in flask framework

### Installing

Folow the code below:

```
$ git clone https://github.com/GregBueno/flask_web
$ conda create -n rasp-flask python=3.6
$ source activate rasp-flask
$ cd flask_web
$ pip install -r requirements.txt
```

If you want to create db, follow the comands below:
```
$ cd ..
$ from flask_web import db,create_app
$ db.create_all(app=create_app())
```

### Running

```
$ cd ..
$ export FLASK_APP=flask_web
$ export FLASK_DEBUG=1
$ flask run
```
