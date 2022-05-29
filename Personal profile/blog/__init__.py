from flask import Flask
# import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '<e8176bb36bf96ca0f4500692b9279ea004292595afb4f024>'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# basedir = os.path.abspath(os.path.dirname(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://c21047868:Yian771012@csmysql.cs.cf.ac.uk:3306/c21047868_flask_lab_db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes
