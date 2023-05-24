from flask import Flask
import os, datetime
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database/database.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'orlandia'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

from control import *

if __name__ == '__main__':
  app.run(port=5000, debug=True)