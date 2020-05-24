from flask import Flask

from helpr.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()
cfg = app.config


@app.route('/')
def hello_world():
    """
    Simple health check route.
    """
    return 'It Lives!'


@app.route('/login_check')
@auth.login_required
def hello_protected_world():
    """
    Simple route to validate whether a user is logged in.
    """
    return {'login': True}


from helpr import helpr_postings, database, auth_handler
