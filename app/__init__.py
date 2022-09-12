from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = b"w9485hj4q30n"
app.config['STATIC_FOLDER'] = 'static'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://test_db:test!1109@localhost:5432/test_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app import models, routes

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
