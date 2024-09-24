import os

from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv

from application.constants import HALF_AN_HOUR
from config.mail import config_mail_server
from config.logging import config_logging
from config.jwt import config_jwt
from users.models import db

from config.routes import config_api
from users.routes import user_api
from password.routes import password_api
from lists.categories.routes import category_api
from lists.headers.routes import header_api

from cli import db_create, db_drop, db_seed

app = Flask(__name__)
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

# Load app configurations
jwt  = config_jwt(app)
mail = config_mail_server(app,Mail)
config_logging(basedir)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'list_maker.db')
db.init_app(app)

#Commands
app.cli.add_command(db_create)
app.cli.add_command(db_drop)
app.cli.add_command(db_seed)

# Routes
@app.route('/')
def hello():
    app.logger.info('Hello World')
    return 'Hello World!'

app.register_blueprint(user_api)
app.register_blueprint(password_api)
app.register_blueprint(config_api)
app.register_blueprint(category_api)
app.register_blueprint(header_api)

if __name__ == '__main__':
    app.run(debug=True) 