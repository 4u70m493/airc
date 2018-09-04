from flask import Flask

# for database ops
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Libs for functionality
import calendar as cal

# Own modules from root dir
from config import Config

# Init everything. Start systems.
app = Flask(__name__)
app.config.from_object(Config) # TODO rewrite to reading a dedicated file
db = SQLAlchemy

from app import routes

if __name__ == '__main__':
    app.run(debug=True)