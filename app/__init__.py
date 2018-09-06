from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

# for database ops
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Own modules from root dir
from config import Config

# Init everything. Start systems.
app = Flask(__name__)
app.config.from_object(Config)   # TODO rewrite to reading a dedicated file
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

if __name__ == '__main__':
    app.run(debug=True)
