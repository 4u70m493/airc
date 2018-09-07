from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask import request
# from flask_nav import Nav
# from flask_nav.elements import Navbar, View

# for database ops
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Own modules from root dir
from config import Config

# Init everything. Start systems.
app = Flask(__name__)
app.config.from_object(Config)   # TODO rewrite to reading a dedicated file
bootstrap = Bootstrap(app)
babel = Babel(app)
# nav = Nav()
#
# @nav.navigation()
# def mynavbar():
#     # TODO construct navbar using information about the user
#     return Navbar(
#         'MyNewWhatever',
#         View('Home', 'index'),
#     )
# nav.init_app(app)
#

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

if __name__ == '__main__':
    app.run()
