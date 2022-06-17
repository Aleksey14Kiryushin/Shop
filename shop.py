#  - Не создается База Данных
#  - Создавать избранные посты
#  + Добработать профиль
#  + Создать страницу регистрации, проверить как после этого работает base.html
#  - В регистрации сделать условие, чтобы нельля было осталять пустыми поля 
#  + Добавить условие, когда нет записей
#  + добавить строку для указания цены


#  + Создавать именно ССЫЛКИ
#  + найти информацию о скачивании изображений

#  - Расположить обьекты сверху скрипта, возможно стоит распологать script только в base
# + разобраться, почему testing не работает, когда находится в папке

#  - отправлять посты из js на flask, потом ТОЛЬКО 3 поста добавлять к записи

# возможность удалять из избранных
# окно создания градиент кнопки https://active-vision.ru/icon/gradient/

# https://habr.com/ru/post/485404/

# input:invalid:required {
#   background-image: linear-gradient(to right, pink, lightgreen);
# }

# <a href="tel:+">awd</a> для звонка

from flask import Flask, redirect, render_template, url_for, request, session, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import imghdr
import os
from random import *

app = Flask(__name__)

# CONFIGS
app.config['SQLAlchemy_DATABASE_URI'] = "sqlite:///ShopBase.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_BINDS'] = False

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

app.config['UPLOAD_PATH'] = 'static/uploads'

app.config['SECRET_KEY'] = os.urandom(32)

# variables
id_shoper = -1

# Data-Bases
DB = SQLAlchemy(app)

class ShopArticle(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(100), nullable=False)
    intro = DB.Column(DB.String(300), nullable=False)

    text = DB.Column(DB.Text, nullable=False)
    date = DB.Column(DB.DateTime, default=datetime.utcnow)

    price = DB.Column(DB.String(100), nullable=False)

    url = DB.Column(DB.Text, nullable=False)
    name_visiable = DB.Column(DB.Text, nullable=False)
    name_invisiable = DB.Column(DB.Text, nullable=False)

    to_favourite = DB.Column(DB.Integer)

    image_1st = DB.Column(DB.Text)
    image_2nd = DB.Column(DB.Text)
    image_3rd = DB.Column(DB.Text)

    def __repr__(self):
        return '<Article %r>' % self.id

class Shoper(DB.Model):
    id_shoper = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    password = DB.Column(DB.String(100), nullable=False)
    like_posts = DB.Column(DB.String(100), nullable=False)


    def __repr__(self):
        return '<Shoper %r>' % self.id_shoper

class Images(DB.Model):
    __tablename__ = "imgs"
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    img = DB.Column(DB.LargeBinary)
      

DB.create_all()

# Downloading Files
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/download/<int:id>/<int:shoper_id>') 
def downloading(id, shoper_id):
    global counter_image
    files = os.listdir(app.config['UPLOAD_PATH'])
    print("FILES", files)
    print(1)
    counter_image = 0
    return render_template('download.html', files=files, id=id, shoper_id=shoper_id)

@app.route('/download/<int:id>/<int:shoper_id>', methods=['POST'])
def upload_files(id, shoper_id):
    global counter_image
    print(2)
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        # проверка на расширение
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
            # download
        
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
       
        # Добавление к посту
        print("FILENAME",filename)
        try:

            post = ShopArticle.query.get(id)

            if counter_image == 0:
                post.image_1st = filename
            elif counter_image == 1:
                post.image_2nd = filename
            elif counter_image == 2:
                post.image_3rd = filename 

            DB.session.commit()

        except Exception as _Ex:
            print("WARNING IN DOWNLOADING")
            print(_Ex)

        print("NOTICE", id)
        counter_image += 1
    
    return 'H1!', 204

@app.route('/download/<int:id>/<int:shoper_id>/uploads/<string:filename>')
def upload(filename, id):
    print(3)
    print("FILENAME2",filename)
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
# 

@app.route("/")
def index_none():
    print("id_shoper", id_shoper)
    if id_shoper == -1:
        return redirect('/log_in/10')
    return render_template("index.html", id_shoper=id_shoper)

@app.route("/<int:id_shoper>")
def index(id_shoper):
    print("id_shoper", id_shoper)
    if id_shoper == -1:
        return redirect('/log_in/10')

    # все посты
    posts = ShopArticle.query.order_by().all()
    the_best_post = None
    random_post = None

    if len(posts) >= 1:
        status = "GOOD"
        all_posts = list()
        the_best_count = 0
        for post in posts:
            if post.to_favourite >= the_best_count:     
                the_best_count = post.to_favourite
                # лучший пост
                the_best_post = post

            all_posts.append(post)
        # рандомный пост
        random_post = choice(all_posts)

        
    else:
        status = "BAD"

    return render_template("index.html", status=status, id_shoper=id_shoper, the_best_post=the_best_post, random_post=random_post)

@app.route("/about/<int:id_shoper>")
def about(id_shoper):
    return render_template("about.html", id_shoper=id_shoper)

@app.route("/posts/<int:id>/<int:id_shoper>", methods=["POST", "GET"])
def post_detail(id, id_shoper):
    post = ShopArticle.query.get(id)

    return render_template("post_detail.html", notice=post, id_shoper=id_shoper)

@app.route("/posts/<int:id_shoper>", methods=["POST", "GET"])
def posts(id_shoper):
    
    notices = ShopArticle.query.order_by(ShopArticle.date.desc()).all()

    return render_template("posts.html", notices=notices, id_shoper=id_shoper)

@app.route("/profile/<int:id_shoper>")
def profile(id_shoper):
    notices = ShopArticle.query.order_by(ShopArticle.date.desc()).all()
    shoper_list = list()

    try:
        shoper = Shoper.query.get(id_shoper)
        shoper_name = shoper.name
    except:
        return redirect('/log_in/2')

    print("SHOPER_NAME", shoper.name)

    for notice in notices:
        if notice.name_invisiable == shoper_name:
            shoper_list.append(notice)

    print("LENGTH", len(notices))

    return render_template("profile.html", notices=shoper_list, id_shoper=id_shoper, shoper_name=shoper_name)

@app.route("/log_in/<int:warning_log>", methods=["POST", "GET"])
def logIn(warning_log):
    if request.method == "POST":
        shoper = False

        name = request.form["name"]
        password = request.form["password"]

        shopers = Shoper.query.order_by().all()
        
        # по всей бд ищем пользователя с такими данными
        for shop in shopers:
            print(f"{shop.name} - {name}")
            print(f"{shop.password} - {password}")
            if shop.name.lower() == name.lower() and shop.password.lower() == password.lower():
                shoper = shop
                print("Shoper Was Found", shoper.id_shoper)

        if not shoper:
            shoper = Shoper(name=name, password=password, 
                            like_posts='')
            try:
                DB.session.add(shoper) 
                DB.session.commit()
                print("CREATE shoper:", shoper.id_shoper)
            except:
                print("WARNING Account")
        
        try:

            print("Shoper_ID",shoper.id_shoper)
            if warning_log == 1:
                return redirect(f'/create-notice/{shoper.id_shoper}/1')
            elif warning_log == 2:
                return redirect(f'/profile/{shoper.id_shoper}')
            else:
                return redirect(f'/{shoper.id_shoper}')

        except Exception as _Ex:
            return str(_Ex)

    else:
        return render_template("log_in.html", warning_log=warning_log)

@app.route("/posts/<int:id>/delete/<int:id_shoper>")
def delete_post(id, id_shoper):
    try:
        post = ShopArticle.query.get_or_404(id)
    except:
        return redirect('/log_in/10')

    try:
        DB.session.delete(post)
        DB.session.commit()
        print("ID_DELETED", id)
        return redirect(f'/{id_shoper}')

    except Exception as _ex:
        return str(_ex)

@app.route("/posts/<int:id>/edit/<int:id_shoper>/<int:log_warning>", methods=["POST", "GET"])
def edit_post(id, id_shoper,log_warning):
    post = ShopArticle.query.get_or_404(id)
    
    if request.method == "POST":
        try:
            shoper = Shoper.query.get(id_shoper)
            print("SHOPER_NAME", shoper.name)
        except:
            return redirect('/log_in/10')

        post.name_invisiable = shoper.name
        post.name_visiable = request.form['name']
        post.title = request.form['title']
        post.url = request.form['url']
        post.intro = request.form['intro']
        post.text = request.form['text']
        post.price = request.form['price']
        
          
        try:
            print(post.id)
            DB.session.commit()
            return redirect(f'/{id_shoper}')

        except Exception as _Ex:
            return str(_Ex)
    
    else:
        name = post.name_invisiable
        title = post.title
        url = post.url
        intro = post.intro
        text = post.text
        price = post.price
        return render_template("testing.html", id_shoper=id_shoper, name=name, title=title, url=url, price=price, intro=intro, text=text)


@app.route("/create-notice/<int:id_shoper>/<int:warning_log>", methods=["POST", "GET"])
def createNotice(id_shoper, warning_log): 
    global list_form

    name = ''
    title = ''
    url = ''
    intro = ''
    text = ''
    price = ''
    img = ''

    if request.method == "POST":
        
        returning = url_for('static', filename = 'check_form.js')
        print("retuning", request.form)
        returning = True
        print(request.form)
        name = request.form['name']
        title = request.form['title']
        url = request.form['url']
        intro = request.form['intro']
        text = request.form['text']
        price = request.form['price']

        list_form = (name, title, url, intro, text, price)
        print(list_form)
        for i in range(len(list_form)):
            if list_form[i] == '':
                returning = False
        
        print("retuning", returning)     
        if returning: #request.form["onsubmit"]
            print("NEW")
            # if id_shoper == None:
            #     print("Следует пройти в log in")
            # else:
            #     print(f"Все ок\nShoper id {id_shoper}")

            try:
                shoper = Shoper.query.get(id_shoper)
                print("SHOPER_NAME", shoper.name)
                shoper_name = shoper.name
            except:
                return redirect('/log_in/1')

            # try:
            #     image = request.form['input_img_1']
            #     print("IMG", image)
            # except:
            #     print("Файлов не найдено!")

            notice = ShopArticle(title=title, intro=intro, text=text, 
                                    name_invisiable=shoper_name, 
                                    name_visiable=name, url=url,
                                    price=price, image_1st='',
                                    image_2nd='', image_3rd='', to_favourite=0) 
            try:
                DB.session.add(notice)
                DB.session.commit()
                print(notice.id)
                return redirect(f'/download/{notice.id}/{id_shoper}')

            except Exception as _Ex:
                return str(_Ex)

    elif warning_log == 1:
        # list_form = (name, title, url, intro, text, price)
        print(list_form)
        name = list_form[0]
        title = list_form[1]
        url = list_form[2]
        intro = list_form[3]
        text = list_form[4]
        price = list_form[5]
      
    return render_template("testing.html", warning_log=warning_log, id_shoper=id_shoper, name=name, title=title, url=url, price=price, intro=intro, text=text)
# @app.route("/posts/<int:id>/<int:id_shoper>/1")
# def like(id, id_shoper):
#     post = ShopArticle.query.get(id)
#     post.likes += 1

#     try:
#         print(post.id)
#         DB.session.commit()

#     except Exception as _Ex:
#         return str(_Ex)

#     try:
#         shoper = Shoper.query.get(int(id_shoper))
#         shoper.like_posts.remove(id, '')
#         shoper.like_posts += f',{id}'
#         DB.session.commit()
#         print("LIKE_POSTS", shoper.like_posts)
#     except:
#         print("WARNING")

#     amount_like = post.likes
#     print(amount_like)

#     return render_template("post_detail.html", notice=post, id_shoper=id_shoper, amount_like=amount_like)

# @app.route("/post/<int:id>/<int:id_shoper>/like")
# def like_in_posts(id, id_shoper):
#     post = ShopArticle.query.get(id)

#     try:
#         print(post.id)
#         DB.session.commit()

#     except Exception as _Ex:
#         return str(_Ex)

#     try:
#         shoper = Shoper.query.get(int(id_shoper))
#         print("Shoper",shoper)
#         print("Shoper_posts",shoper.like_posts)
#         shoper.like_posts += f' {id}'
#         DB.session.commit()
#         print("LIKE_POSTS", shoper.like_posts)
#     except:
#         print("WARNING")

#     return render_template("post_detail.html", notice=post, id_shoper=id_shoper)

@app.route("/favourite/<int:id_shoper>")
def favourites(id_shoper):

    try:   
        shoper = Shoper.query.get(id_shoper)
        print(shoper)
        favourite_posts = shoper.like_posts
        print(shoper.name)
    except:
        return redirect('/log_in/10')

    list_liked_posts = list()

    # favourite_posts.split(' ')
    print("Favourites post",str(favourite_posts))

    favourite_posts = str(favourite_posts).split()

    for i in range(len(favourite_posts)):
        try:
            print("COUNTER", i)
            print(favourite_posts[i])     
            post = ShopArticle.query.get(int(favourite_posts[i]))
            print(post)
            print(post.title)
            list_liked_posts.append(post)
        except:
            print("WARNING")
    
    # переворачиваем список
    list_liked_posts = list_liked_posts[::-1]

    return render_template("favourite.html", notices=list_liked_posts, id_shoper=id_shoper)

@app.route("/posts/<int:id>/<int:id_shoper>/favourite")
def like(id, id_shoper):
    post = ShopArticle.query.get(id)

    try:
        post.to_favourite += 1
        print("Нужно добавить в избранное POST", post.name_visiable)
        DB.session.commit()
        print("Всего добавлено в избранное:", post.to_favourite)
    
    except Exception as _Ex:
        return str(_Ex)

    try:
        shoper = Shoper.query.get(int(id_shoper))
        print("Shoper",shoper)
        print("Shoper_posts",shoper.like_posts)
        if not (str(id) in str(shoper.like_posts)):
            shoper.like_posts += f' {id}'
            DB.session.commit()
        print("LIKE_POSTS", shoper.like_posts)
    except:
        print("WARNING")

    
    # posts = ShopArticle.query.order_by(ShopArticle.date.desc()).all()

    return render_template("post_detail.html", notice=post, id_shoper=id_shoper)

@app.route("/posts/<int:id>/<int:id_shoper>/del_favourite")
def delete_favourite(id, id_shoper):
    try:
        shoper = Shoper.query.get_or_404(id_shoper)
    except:
        return redirect('/log_in/10')

    try:
        shoper_liked_posts = shoper.like_posts.split()
        print("shoper_liked_posts 0", shoper_liked_posts)
        for post in shoper_liked_posts:
            print(post)
            if post == str(id):
                print("POST Deleted", post)
                shoper_liked_posts.remove(post)
                print("shoper_liked_posts1",shoper_liked_posts)
                break
        print("shoper_liked_posts 11",shoper_liked_posts)

        like_posts = ''
        if len(shoper_liked_posts) >= 1:
            for shop in shoper_liked_posts:
                print("post", shop)
                like_posts += f' {shop}'
            shoper.like_posts = like_posts
        else:
            shoper.like_posts = ''

        DB.session.commit()
        print("shoper_liked_posts2",shoper.like_posts)
        print("ID_DELETED", id)
        return redirect(f'/{id_shoper}')

    except Exception as _ex:
        return str(_ex)

if __name__ == "__main__":
    app.run(debug=True)
