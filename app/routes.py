import json
import os

from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.models import User, Ad


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for("login"))


@app.errorhandler(401)
def unauthorized(e):
    flash("Вы не авторизованы")
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for("home"))
            else:
                flash("Извините, неправильный логин или пароль")
                return redirect(url_for("login"))
        else:
            flash("Пожалуйста, введите логин и пароль")
            return redirect(url_for("login"))
    elif request.method == "GET":
        if "userLoggedIn" in session:
            flash(f"Вы уже авторизованы")
            return redirect(url_for("index"))
        else:
            return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта")
    return redirect(url_for("login"))


@app.route('/home')
@login_required
def home():
    if current_user.access_level in [1, 2, 3]:
        return render_template("home.html", access_level=current_user.access_level, ads=Ad.query.all())
    else:
        flash("У вас нет доступа к этой странице")
        return redirect(url_for("login"))


@app.route('/delete_ad/<int:ad_id>', methods=['POST'])
@login_required
def delete_ad(ad_id):
    if current_user.access_level in [1, 2, 3]:
        ad = Ad.query.filter_by(id=ad_id).first()
        db.session.delete(ad)
        db.session.commit()
        flash("Объявление удалено")
        return redirect(url_for("home"))
    else:
        flash("У вас нет доступа к этой странице")
        return redirect(url_for("login"))


def delete_img(img):
    file_path = os.path.join(app.root_path, "static\\img", img)
    try:
        os.chmod(file_path, 0o777)
        os.remove(file_path)
    except FileNotFoundError:
        pass


@app.route('/clear_ads', methods=['GET', 'POST'])
@login_required
def clear_ads():
    if current_user.access_level in [1, 2, 3]:
        for ad in Ad.query.all():
            if ad.image:
                delete_img(ad.image)
            db.session.delete(ad)
        db.session.commit()
        flash("Объявления удалены")
        return redirect(url_for("home"))


@app.route('/get_ads_list', methods=['GET'])
@login_required
def get_ads_list():
    if current_user.access_level in [1, 2, 3]:
        ads = Ad.query.all()
        print(len(ads))
        ads_list = []
        for i in range(current_user.access_level*100):
            if i < len(ads):
                ad = ads[i]
                ads_list.append({
                    "id": ad.id,
                    "title": ad.title,
                    "price": ad.price,
                    "currency": ad.currency,
                    "image": ad.image,
                    "seller": ad.seller
                })
            else:
                break
        return json.dumps(ads_list)
    else:
        flash("У вас нет доступа к этой странице")
        return redirect(url_for("login"))


def add_user(username, password, access_level):
    print("Adding user...")
    user = User(username=username, password_hash=generate_password_hash(password), access_level=access_level)
    db.session.add(user)
    db.session.commit()
    print("User added")


if __name__ == '__main__':
    app.run(debug=True)
