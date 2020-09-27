import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
import stripe

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'mysecret'
app.config['CACHE_TYPE'] = "simple"
app.config['CACHE_DEFAULT_TIMEOUT'] = 0

basedir = os.path.abspath(os.path.dirname(__file__))
path = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

public_key = "pk_test_TYooMQauvdEDq54NiTphI7jx"
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

db = SQLAlchemy(app)
Migrate(app, db)
cache = Cache(app)

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"

###########################
#### BLUEPRINT CONFIGS #######
#########################


# register your blueprints here
from companyBlog.users.views import users
from companyBlog.blogposts.views import blogposts
from companyBlog.core.views import core
from companyBlog.error_pages.handlers import error_pages

app.register_blueprint(blogposts)
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
