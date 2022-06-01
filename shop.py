# Не создается База Данных
# Создавать избранные посты

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

    def __repr__(self):
        return '<Article %r>' % self.id

DB.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/posts/<int:id>")
def post_detail(id):
    post = ShopArticle.query.get(id)

    return render_template("post_detail.html", notice=post)

@app.route("/posts")
def posts():
    notices = ShopArticle.query.order_by(ShopArticle.date.desc()).all()

    return render_template("posts.html", notices=notices)

@app.route("/create-notice", methods=["POST", "GET"])
def createNotice():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        notice = ShopArticle(title=title, intro=intro, text=text)

        try:
            DB.session.add(notice)
            DB.session.commit()
            return redirect('/')

        except Exception as _Ex:
            return str(_Ex)
    else:
        return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)
