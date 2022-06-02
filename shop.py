# Не создается База Данных
# Создавать избранные посты
# Добработать профиль
# Создать страницу регистрации, проверить как после этого работает base.html
# В регистрации сделать условие, чтобы нельля было осталять пустыми поля 
# Добавить условие, когда нет записей

from flask import Flask, redirect, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLAlchemy_DATABASE_URI'] = "sqlite:///ShopBase.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_BINDS'] = False

DB = SQLAlchemy(app)

class ShopArticle(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(100), nullable=False)
    intro = DB.Column(DB.String(300), nullable=False)

    text = DB.Column(DB.Text, nullable=False)
    date = DB.Column(DB.DateTime, default=datetime.utcnow)

    url = DB.Column(DB.Text, nullable=False)
    name_visiable = DB.Column(DB.Text, nullable=False)
    name_invisiable = DB.Column(DB.Text, nullable=False)


    def __repr__(self):
        return '<Article %r>' % self.id

class Shoper(DB.Model):
    id_shoper = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    password = DB.Column(DB.String(100), nullable=False)

    def __repr__(self):
        return '<Shoper %r>' % self.id_shoper

DB.create_all()

@app.route("/<int:id_shoper>")
def index(id_shoper):
    return render_template("index.html", id_shoper=id_shoper)

@app.route("/about/<int:id_shoper>")
def about(id_shoper):
    return render_template("about.html", id_shoper=id_shoper)

@app.route("/posts/<int:id>/<int:id_shoper>")
def post_detail(id, id_shoper):
    post = ShopArticle.query.get(id)

    return render_template("post_detail.html", notice=post, id_shoper=id_shoper)

@app.route("/posts/<int:id_shoper>")
def posts(id_shoper):
    notices = ShopArticle.query.order_by(ShopArticle.date.desc()).all()

    return render_template("posts.html", notices=notices, id_shoper=id_shoper)

@app.route("/profile/<int:id_shoper>")
def profile(id_shoper):
    notices = ShopArticle.query.order_by(ShopArticle.date.desc()).all()
    shoper_list = list()

    shoper = Shoper.query.get(id_shoper)
    shoper_name = shoper.name

    for notice in notices:
        if notice.name_invisiable == shoper_name:
            shoper_list.append(notice)

    return render_template("profile.html", notices=shoper_list, id_shoper=id_shoper, shoper_name=shoper_name)

@app.route("/log_in", methods=["POST", "GET"])
def logIn():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        shoper = Shoper(name=name, password=password)

        try:
            DB.session.add(shoper)
            DB.session.commit()
            print("Shoper_ID",shoper.id_shoper)

            return redirect(f'/{shoper.id_shoper}')

        except Exception as _Ex:
            return str(_Ex)

    else:
        return render_template("log_in.html")

@app.route("/create-notice/<int:id_shoper>", methods=["POST", "GET"])
def createNotice(id_shoper):
    if request.method == "POST":
        shoper = Shoper.query.get(id_shoper)
        print("SHOPER_NAME", shoper.name)
        shoper_name = shoper.name

        name = request.form['name']
        title = request.form['title']
        url = request.form['url']
        intro = request.form['intro']
        text = request.form['text']

        notice = ShopArticle(title=title, intro=intro, text=text, 
                                name_invisiable=shoper_name, 
                                name_visiable=name, url=url)
        try:
            DB.session.add(notice)
            print(notice.id)
            DB.session.commit()
            return redirect(f'/{id_shoper}')

        except Exception as _Ex:
            return str(_Ex)
    else:
        return render_template("create.html", id_shoper=id_shoper)

if __name__ == "__main__":
    app.run(debug=True)
