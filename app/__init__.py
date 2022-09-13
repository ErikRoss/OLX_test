import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.secret_key = b"w9485hj4q30n"
app.config['STATIC_FOLDER'] = 'static'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://test_db:test!1109@localhost:5432/test_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app import models, routes, parser

db.create_all()


@socketio.on('parse ads')
def parse_ads():
    print("Parsing ads...")
    par = parser.Parser()
    url = "https://www.olx.ua/d/uk/elektronika/telefony-i-aksesuary/?search%5Bphotos%5D=1"
    limit = current_user.access_level * 100
    par.collect_ads(socketio, url, limit)
    print("Ads parsed")


@socketio.on('delete ad')
def delete_ad(ad_id):
    if current_user.access_level in [1, 2, 3]:
        ad = models.Ad.query.filter_by(id=int(ad_id)).first()
        print(ad)
        db.session.delete(ad)
        db.session.commit()
        delete_img(ad.image)
        emit("delete ad", ad_id)
        print("Ad deleted")
        disconnect()


def delete_img(img):
    file_path = os.path.join(app.root_path, "static\\img", img)
    try:
        os.chmod(file_path, 0o777)
        os.remove(file_path)
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    app.run(debug=True)
