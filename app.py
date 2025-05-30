import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime
import country_converter as coco


db = SQL("sqlite:///databases.db")
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route('/', methods=['GET'])
@login_required
def index():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    posts = db.execute("SELECT * FROM posts ORDER BY totalvote DESC")
    currentusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    friends = db.execute("SELECT * FROM :friends",
                         friends = username + "_friends")
    return render_template("index.html",posts = posts, userid = user_id, username = username, currentusername = currentusername, friends = friends)

@app.route('/filternovel', methods=['GET'])
@login_required
def filternovel():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    posts = db.execute("SELECT * FROM posts WHERE type = :type ORDER BY totalvote DESC", type = "novel")
    currentusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    friends = db.execute("SELECT * FROM :friends",
                         friends = username + "_friends")
    return render_template("index.html",posts = posts, userid = user_id, username = username, currentusername = currentusername, friends = friends)

@app.route('/filterfiction', methods=['GET'])
@login_required
def filterfiction():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    posts = db.execute("SELECT * FROM posts WHERE type = :type ORDER BY totalvote DESC", type = "fiction")
    currentusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    friends = db.execute("SELECT * FROM :friends",
                         friends = username + "_friends")
    return render_template("index.html",posts = posts, userid = user_id, username = username, currentusername = currentusername, friends = friends)

@app.route('/filterstorybook', methods=['GET'])
@login_required
def filterstorybook():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    posts = db.execute("SELECT * FROM posts WHERE type = :type ORDER BY totalvote DESC", type = "storybook")
    currentusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    friends = db.execute("SELECT * FROM :friends",
                         friends = username + "_friends")
    return render_template("index.html",posts = posts, userid = user_id, username = username, currentusername = currentusername, friends = friends)

@app.route('/filterhistory', methods=['GET'])
@login_required
def filterhistory():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    posts = db.execute("SELECT * FROM posts WHERE type = :type ORDER BY totalvote DESC", type = "history")
    currentusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    friends = db.execute("SELECT * FROM :friends",
                         friends = username + "_friends")
    return render_template("index.html",posts = posts, userid = user_id, username = username, currentusername = currentusername, friends = friends)

@app.route('/filterpoetry', methods=['GET'])
@login_required
def filterpoetry():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    posts = db.execute("SELECT * FROM posts WHERE type = :type ORDER BY totalvote DESC", type = "poetry")
    currentusername = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    friends = db.execute("SELECT * FROM :friends",
                         friends = username + "_friends")
    return render_template("index.html",posts = posts, userid = user_id, username = username, currentusername = currentusername, friends = friends)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        gender = request.form.get("gender")
        country = request.form.get("country")
        email = request.form.get("email")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        if password != confirmation:
            flash("The passwords doesn't match!")
            return redirect("/register")

        flag = 0
        while True:
            if (len(password)<=8):
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            else:
                flag = 0
                break

        if flag == -1:
            flash("Your password must have minimum length of 8 and must contain capital, noncapital characters and numbers!")
            return redirect("/register")
        hashed_password = generate_password_hash(password)
        allusersnames = db.execute("SELECT username FROM users")
        anotherlist = []
        for x in allusersnames:
            for item in x.values():
                anotherlist.append(item)
        print(anotherlist)
        if username in anotherlist:
            flash("This username has already been taken!")
            return redirect("/register")
        else:
            db.execute("INSERT INTO users (name,surname,username, password, gender, country, email, day, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",name,surname,username,hashed_password,gender,country,email,day,month,year)
            db.execute("CREATE TABLE :friends (id integer PRIMARY KEY AUTOINCREMENT , friendname text, friendid integer)", friends = username + "_friends")
            return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        rows2 = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            if len(rows2) != 1 or not check_password_hash(rows2[0]["password"], request.form.get("password")):
                flash("invalid username/email and/or password")
                return render_template("login.html")



        if len(rows) == 1 and check_password_hash(rows[0]["password"], request.form.get("password")):
            session["user_id"] = rows[0]["id"]
        # Remember which user has logged in
        elif len(rows2) == 1 and check_password_hash(rows2[0]["password"], request.form.get("password")):
            session["user_id"] = rows2[0]["id"]
        else:
            flash("invalid username/email and/or password")
            return render_template("login.html")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST":
        booktype = request.form.get("booktype")
        title = request.form.get("title")
        subject = request.form.get("subject")
        content = request.form.get("postcontent")

        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        db.execute("INSERT INTO posts (type, title, subject, content, username, user_id) VALUES (?, ?, ?, ?, ?, ?)", booktype, title, subject, content, username, id)

        return redirect("/")
    else:
        userid = session["user_id"]
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        return render_template("post.html", username= username, userid = userid)

@app.route("/bigpost/users/<username>/<int:postid>", methods=["GET", "POST"])
def bigpost(username, postid):
    postname = db.execute("SELECT username FROM posts WHERE id =?", postid)[0]["username"]
    title = db.execute("SELECT title FROM posts WHERE id = ?", postid)[0]["title"]
    content = db.execute("SELECT content FROM posts WHERE id = ?", postid)[0]["content"]
    subject = db.execute("SELECT subject FROM posts WHERE id = ?", postid)[0]["subject"]
    upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
    downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
    Booktype = db.execute("SELECT type FROM posts WHERE id = ?", postid)[0]["type"]
    date_time = db.execute("SELECT datetime FROM posts WHERE id = ?", postid)[0]["datetime"]
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    userid = session["user_id"]
    comments = db.execute("SELECT * FROM comments WHERE postid = :postid",
                          postid = postid)

    postuserid = db.execute("SELECT user_id FROM posts WHERE id = ?", postid)[0]["user_id"]
    currentuser = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    friends = db.execute("SELECT * FROM :friends",
                         friends = currentuser + "_friends")
    return render_template("bigpost.html",postname = postname, title = title, content = content, subject = subject, upvote = upvote, downvote = downvote, type = Booktype, comments = comments, date_time = date_time,
                           username = username, userid = userid, postid = postid, postuserid = postuserid, friends = friends)


@app.route("/profile/users/<username>/<int:userid>", methods=["GET","POST"])
def findprofile(userid, username):
    posts = db.execute("SELECT * FROM posts WHERE user_id = ?", userid)
    user = db.execute("SELECT * FROM users WHERE id = ?", userid)
    posts = db.execute("SELECT * FROM posts WHERE user_id  = ? ORDER BY datetime DESC", userid)
    email = db.execute("SELECT email FROM users WHERE id = ?", userid)[0]["email"]
    day = db.execute("SELECT day FROM users WHERE id = ?", userid)[0]["day"]
    month = db.execute("SELECT month FROM users WHERE id = ?", userid)[0]["month"]
    year = db.execute("SELECT year FROM users WHERE id = ?", userid)[0]["year"]
    currentyear = datetime.now().year
    age = currentyear - year
    countrycode = db.execute("SELECT country FROM users WHERE id = ?", userid)[0]["country"]
    some_names = countrycode
    cc = coco.CountryConverter()
    username = db.execute("SELECT username FROM users WHERE id = ?", userid)[0]["username"]
    country = cc.convert(names = some_names, to = 'name_short')
    follower = db.execute("SELECT followers FROM users WHERE id = ?", userid)[0]["followers"]
    following = db.execute("SELECT followings FROM users WHERE id = ?", userid)[0]["followings"]
    bio = db.execute("SELECT bio FROM users WHERE id = ?", userid)[0]["bio"]
    if userid == session["user_id"]:
        profilesetting = 1
    else:
        profilesetting = 0
    currentuser = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    currentuserid = session["user_id"]
    friend = db.execute("SELECT friendname FROM :userfriends WHERE friendname = :friendname", userfriends = currentuser + "_friends", friendname = username)
    friends = db.execute("SELECT * FROM :friends",
                         friends = currentuser + "_friends")
    return render_template("profile.html", posts = posts, user = user,username = username, userid = userid, email = email, day = day, month = month, year = year, age = age, country = country,
                           followers = follower, followings = following, bio = bio, profilesetting = profilesetting, currentuser = currentuser, currentuserid = currentuserid, friend = friend, friends = friends)


@app.route("/upvote/<int:postid>", methods=["GET", "POST"])
def upvote(postid):
    try:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]

        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1
            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = 0
            upvote = upvote-1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 0 and downvoted == -1:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
    except:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        db.execute("INSERT INTO updownvoted (username, userid, postid, upvoted, downvoted) VALUES (?, ?, ?, ?, ?)",
               username,
               session["user_id"],
               postid,
               0,
               0)
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]

        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = 0
            upvote = upvote-1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 0 and downvoted == -1:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")

@app.route("/downvote/<int:postid>", methods=["GET", "POST"])
def downvote(postid):
    try:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]

        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            upvote = upvote - 1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 0 and downvoted == -1:
            upvoted = 0
            downvoted = 0
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")

    except:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        db.execute("INSERT INTO updownvoted (username, userid, postid, upvoted, downvoted) VALUES (?, ?, ?, ?, ?)",
               username,
               session["user_id"],
               postid,
               0,
               0)
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]

        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            upvote = upvote - 1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")
        elif upvoted == 0 and downvoted == -1:
            upvoted = 0
            downvoted = 0
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/")

@app.route("/upvote2/<int:postid>", methods=["GET", "POST"])
def upvote2(postid):
    try:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]
        postername = db.execute("SELECT username FROM posts WHERE id = ?", postid)[0]["username"]
        posterid = db.execute("SELECT user_id FROM posts WHERE id = ?", postid)[0]["user_id"]
        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1
            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = 0
            upvote = upvote-1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 0 and downvoted == -1:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
    except:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        db.execute("INSERT INTO updownvoted (username, userid, postid, upvoted, downvoted) VALUES (?, ?, ?, ?, ?)",
               username,
               session["user_id"],
               postid,
               0,
               0)
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]
        postername = db.execute("SELECT username FROM posts WHERE id = ?", postid)[0]["username"]
        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        posterid = db.execute("SELECT user_id FROM posts WHERE id = ?", postid)[0]["user_id"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = 0
            upvote = upvote-1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 0 and downvoted == -1:
            upvoted = 1
            downvoted = 0
            upvote = upvote + 1
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))

@app.route("/downvote2/<int:postid>", methods=["GET", "POST"])
def downvote2(postid):
    try:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]
        postername = db.execute("SELECT username FROM posts WHERE id = ?", postid)[0]["username"]
        posterid = db.execute("SELECT user_id FROM posts WHERE id = ?", postid)[0]["user_id"]
        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            upvote = upvote - 1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 0 and downvoted == -1:
            upvoted = 0
            downvoted = 0
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))

    except:
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        db.execute("INSERT INTO updownvoted (username, userid, postid, upvoted, downvoted) VALUES (?, ?, ?, ?, ?)",
               username,
               session["user_id"],
               postid,
               0,
               0)
        downvoted = db.execute("SELECT downvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["downvoted"]
        upvoted = db.execute("SELECT upvoted FROM updownvoted WHERE username = ? and userid = ? and postid = ?", username, session["user_id"], postid)[0]["upvoted"]
        postername = db.execute("SELECT username FROM posts WHERE id = ?", postid)[0]["username"]
        posterid = db.execute("SELECT user_id FROM posts WHERE id = ?", postid)[0]["user_id"]
        downvote = db.execute("SELECT downvote FROM posts WHERE id = ?", postid)[0]["downvote"]
        upvote = db.execute("SELECT upvote FROM posts WHERE id = ?", postid)[0]["upvote"]
        if upvoted == 0 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)


            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 1 and downvoted == 0:
            upvoted = 0
            downvoted = -1
            upvote = upvote - 1
            downvote = downvote - 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, posterid))
        elif upvoted == 0 and downvoted == -1:
            upvoted = 0
            downvoted = 0
            downvote = downvote + 1

            db.execute("UPDATE updownvoted SET upvoted = :upvoted WHERE username = :username and userid = :userid and postid = :postid",
                       upvoted = upvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE updownvoted SET downvoted = :downvoted WHERE username = :username and userid = :userid and postid = :postid",
                       downvoted = downvoted,
                       username = username,
                       userid = session["user_id"],
                       postid = postid)

            db.execute("UPDATE posts SET upvote = :upvote WHERE id = :bookid",
                        upvote = upvote,
                        bookid = postid)
            db.execute("UPDATE posts SET downvote = :downvote WHERE id = :bookid",
                        downvote = downvote,
                        bookid = postid)
            db.execute("UPDATE posts SET totalvote = :upvote + :downvote WHERE id = :bookid",
                        upvote = upvote,
                        downvote = downvote,
                        bookid = postid)
            return redirect("/profile/users/%s/%s"%(postername, session["user_id"]))

@app.route("/search", methods=["POST"])
def search():
    text = request.form.get("text")
    if text == "":
        return redirect("/")
    results = db.execute("SELECT * FROM users WHERE username LIKE :text", text = '%' + text + '%')
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    userid = session["user_id"]

    postresults = db.execute("SELECT * FROM posts WHERE subject LIKE :text", text = '%' + text + '%')
    postresults2 = db.execute("SELECT * FROM posts WHERE title LIKE :text", text = '%' + text + '%')
    postresults3 = db.execute("SELECT * FROM posts WHERE content LIKE :text", text = '%' + text + '%')
    postinfos = []
    if not postresults:
        if not postresults2:
            if not postresults3:
                postinfos = postresults
            else:
                postinfos = postresults3
        else:
            postinfos = postresults2
    else:
        postinfos = postresults
    friends = db.execute("SELECT * FROM :friends",
                         friends = username + "_friends")

    return render_template("results.html", username = username , userid = userid, results = results, postinfos = postinfos, friends = friends)

@app.route("/editprofile", methods=["GET","POST"])
def editprofile():
    userid = session["user_id"]
    ebio = request.form.get("bio")
    ename = request.form.get("name")
    esurname = request.form.get("surname")
    eusername = request.form.get("username")

    bioc = db.execute("SELECT bio FROM users WHERE id = ?", userid)[0]["bio"]
    namec = db.execute("SELECT name FROM users WHERE id = ?", userid)[0]["name"]
    surnamec = db.execute("SELECT surname FROM users WHERE id = ?", userid)[0]["surname"]
    usernamec = db.execute("SELECT username FROM users WHERE id = ?", userid)[0]["username"]

    currentpassword = request.form.get("password")
    passwords = db.execute(
            "SELECT password FROM users WHERE id = ? ", session["user_id"]
        )[0]["password"]

    if not check_password_hash(passwords, currentpassword):
        flash("Your Current password ain't right")
        return redirect("/profile/users/%s/%s"%(usernamec, userid))

    else:
        if ebio:
            db.execute("UPDATE users SET bio = :bio WHERE id = :id",
                    bio = ebio,
                    id = session["user_id"])
        if ename:
            db.execute("UPDATE users SET name = :ename WHERE id = :id",
                    ename = ename,
                    id = session["user_id"])
        if esurname:
            db.execute("UPDATE users SET surname = :esurname WHERE id = :id",
                    esurname = esurname,
                    id = session["user_id"])
        if eusername:
            db.execute("UPDATE users SET username = :eusername WHERE id = :id",
                    eusername = eusername,
                    id = session["user_id"])

        return redirect("/profile/users/%s/%s"%(usernamec, userid))

@app.route("/changepassword", methods=["GET","POST"])
def changepassword():
    if request.method == "POST":
        currentpassword = request.form.get("currentpassword")
        newpassword = request.form.get("newpassword")
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
        passwords = db.execute(
            "SELECT password FROM users WHERE id = ? ", session["user_id"]
        )[0]["password"]

        hashed_password = generate_password_hash(newpassword)

        if not check_password_hash(passwords, currentpassword):
            flash("Your Current password ain't right")
            return redirect("/profile/users/%s/%s"%(username, session["user_id"]))

        db.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            hashed_password,
            session["user_id"],
        )

        return redirect("/profile/users/%s/%s"%(username, session["user_id"]))


@app.route("/addcomment/<int:postid>/<int:userid>", methods=["GET", "POST"])
def addcomment(postid, userid):
    comment = request.form.get("comment")
    username = db.execute("SELECT username FROM posts WHERE id = ?", postid)
    username2 = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    if comment == "":
        return redirect(url_for('bigpost', username = username, postid = postid))
    db.execute("INSERT INTO comments (comment,postid, userid, username) VALUES (?, ?, ?, ?)",
               comment, postid, session["user_id"], username2)
    return redirect(url_for('bigpost', username = username, postid = postid))

@app.route("/deletepost/<int:postid>",methods=["GET", "POST"])
def deletepost(postid):
    db.execute("DELETE FROM posts WHERE id = ?", postid)

    return redirect("/")

@app.route("/deletecomment/<int:commentid>/<postname>/<int:postid>",methods=["GET", "POST"])
def deletecomment(commentid, postname, postid):
    db.execute("DELETE FROM comments WHERE id = ?", commentid)

    return redirect(url_for('bigpost', username = postname, postid = postid))


@app.route("/follow/<int:userid>/<username>", methods=["GET", "POST"])
def follow(userid, username):
    currentuserid = session["user_id"]
    currentusername = db.execute("SELECT username FROM users WHERE id = ? ", currentuserid)[0]["username"]

    db.execute("INSERT INTO :friends (friendname, friendid) VALUES (:friendname, :friendid)",
               friends = currentusername + "_friends",
               friendname = username,
               friendid = userid)
    db.execute("UPDATE users SET followings = followings + 1 WHERE username = :username AND id = :userid ",
               username = currentusername,
               userid = currentuserid)
    db.execute("UPDATE users SET followers = followers + 1 WHERE username = :username AND id = :userid",
               username = username,
               userid = userid)

    return redirect("/profile/users/%s/%s"%(username, userid))

@app.route("/unfollow/<int:userid>/<username>", methods=["GET","POST"])
def unfollow(userid, username):
    currentuserid = session["user_id"]
    currentusername = db.execute("SELECT username FROM users WHERE id = ? ", currentuserid)[0]["username"]
    db.execute("DELETE FROM :friends WHERE friendname = :friendname AND friendid = :friendid",
               friends = currentusername + "_friends",
               friendname = username,
               friendid = userid)

    db.execute("UPDATE users SET followings = followings - 1 WHERE username = :username AND id = :userid ",
               username = currentusername,
               userid = currentuserid)
    db.execute("UPDATE users SET followers = followers - 1 WHERE username = :username AND id = :userid",
               username = username,
               userid = userid)

    return redirect("/profile/users/%s/%s"%(username, userid))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
