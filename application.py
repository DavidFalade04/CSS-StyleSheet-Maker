import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

    # Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#db
db = SQL("sqlite:///template.db")


@app.route("/")
def home():

    if session.get("user_id") is None:
        return redirect("/login")

    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        invalid = False
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html",invalid = invalid)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html",invalid = invalid)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html",invalid = invalid)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    invalid = False
    if request.method == "GET":
        return render_template("register.html")
    else:
        invalid = False
        if not request.form.get("username"):
            return render_template("register.html",invalid = invalid)

    # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html",invalid = invalid)

    #load in values
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

    #check if password and confirmation match
        if password != confirmation:
            return render_template("register.html",invalid = invalid)
        elif len(password) < 8:
            return render_template("register.html", char = invalid)
        elif intcheck(password) == False:
            return render_template("register.html",intreq = invalid)

        else:
    #check if username exist
            rows = db.execute("SELECT username FROM users WHERE username = :username", username=username)
            if len(rows) != 0:
                return render_template("register.html",usertaken  = invalid)
        #insert in db
        password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:name, :password)", name=username, password=password)
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("register.html")



@app.route("/preset1")
def preset1():
    #check for login
    if session.get("user_id") is None:
        return redirect("/login")


    return redirect("/edit")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    #check for login
    if session.get("user_id") is None:
        return redirect("/login")

    if request.method == "POST":
        #update values
        if request.form.get("allbanners"):
            color = request.form.get("allbanners")
            db.execute("UPDATE sessions SET color = :color WHERE element = :element AND session_id = :session_id OR element = :element2 AND session_id = :session_id", color = color, element = "bannerone", session_id = session["id"], element2 = "mainbanner")
        if request.form.get("allbannersfnt"):
            font = request.form.get("allbannersfnt")
            db.execute("UPDATE sessions SET font = :font WHERE element = :element AND session_id = :session_id OR element = :element2 AND session_id = :session_id", font = font, element = "bannerone", session_id = session["id"], element2 = "mainbanner")
        if request.form.get("allbannersfntsz"):
            fontsize = request.form.get("allbannersfntsz")
            if fontsize.isnumeric() ==  True:
                fontsize = fontsize+ "px"
            db.execute("UPDATE sessions SET fontsize = :fontsize WHERE element = :element AND session_id = :session_id OR element = :element2 AND session_id = :session_id", fontsize = fontsize, element = "bannerone", session_id = session["id"], element2 = "mainbanner")
        if request.form.get("allbannerstxtcolor"):
            textcolor = request.form.get("allbannerstxtcolor")
            db.execute("UPDATE sessions SET textcolor = :textcolor WHERE element = :element AND session_id = :session_id OR element = :element2 AND session_id = :session_id", textcolor = textcolor, element = "bannerone", session_id = session["id"], element2 = "mainbanner")
        if request.form.get("allbannersht"):
            height = request.form.get("allbannersht")
            db.execute("UPDATE sessions SET height = :height WHERE element = :element AND session_id = :session_id OR element = :element2 AND session_id = :session_id", height = height, element = "bannerone", session_id = session["id"], element2 = "mainbanner")
        if request.form.get("allbannerswt"):
            width = request.form.get("allbannerswt")
            db.execute("UPDATE sessions SET width = :width WHERE element = :element AND session_id = :session_id OR element = :element2 AND session_id = :session_id", width = width, element = "bannerone", session_id = session["id"], element2 = "mainbanner")






        if request.form.get("bannerone"):
            color = request.form.get("bannerone")
            db.execute("UPDATE sessions SET color = :color WHERE element = :element AND session_id = :session_id", color = color, element = "bannerone", session_id = session["id"])
        if request.form.get("banneronefnt"):
            font = request.form.get("banneronefnt")
            db.execute("UPDATE sessions SET font = :font WHERE element = :element AND session_id = :session_id", font = font, element = "bannerone", session_id = session["id"])
        if request.form.get("banneronefnt-sz"):
            fontsize = request.form.get("banneronefnt-sz")
            if fontsize.isnumeric() ==  True:
                fontsize = fontsize+ "px"
            db.execute("UPDATE sessions SET fontsize = :fontsize WHERE element = :element AND session_id = :session_id", fontsize = fontsize, element = "bannerone", session_id = session["id"])
        if request.form.get("banneronetxtcolor"):
            textcolor = request.form.get("banneronetxtcolor")
            db.execute("UPDATE sessions SET textcolor = :textcolor WHERE element = :element AND session_id = :session_id", textcolor = textcolor, element = "bannerone", session_id = session["id"])
        if request.form.get("banneroneht"):
            height = request.form.get("banneroneht")
            db.execute("UPDATE sessions SET height = :height WHERE element = :element AND session_id = :session_id", height = height, element = "bannerone", session_id = session["id"])
        if request.form.get("banneronewt"):
            width = request.form.get("banneronewt")
            db.execute("UPDATE sessions SET width = :width WHERE element = :element AND session_id = :session_id", width = width, element = "bannerone", session_id = session["id"])





        if request.form.get("mainbanner"):
            color = request.form.get("mainbanner")
            db.execute("UPDATE sessions SET color = :color WHERE element = :element AND session_id = :session_id", color = color, element = "mainbanner", session_id = session["id"])
        if request.form.get("mainbnrfnt"):
            font = request.form.get("mainbnrfnt")
            db.execute("UPDATE sessions SET font = :font WHERE element = :element AND session_id = :session_id", font = font, element = "mainbanner", session_id = session["id"])
        if request.form.get("mainbnrfnt-sz"):
            fontsize = request.form.get("mainbnrfnt-sz")
            if fontsize.isnumeric() ==  True:
                fontsize = fontsize+ "px"
            db.execute("UPDATE sessions SET fontsize = :fontsize WHERE element = :element AND session_id = :session_id", fontsize = fontsize, element = "mainbanner", session_id = session["id"])
        if request.form.get("mainbnrtxtcolor"):
            textcolor = request.form.get("mainbnrtxtcolor")
            db.execute("UPDATE sessions SET textcolor = :textcolor WHERE element = :element AND session_id = :session_id", textcolor = textcolor, element = "mainbanner", session_id = session["id"])
        if request.form.get("mainbnrht"):
            height = request.form.get("mainbnrht")
            db.execute("UPDATE sessions SET height = :height WHERE element = :element AND session_id = :session_id", height = height, element = "mainbanner", session_id = session["id"])
        if request.form.get("mainbnrwt"):
            width = request.form.get("mainbnrwt")
            db.execute("UPDATE sessions SET width = :width WHERE element = :element AND session_id = :session_id", width = width, element = "mainbanner", session_id = session["id"])

        if request.form.get("bodycolor"):
            color = request.form.get("bodycolor")
            db.execute("UPDATE sessions SET color = :color WHERE element = :element AND session_id = :session_id", color = color, element = "divbody", session_id = session["id"])
        if request.form.get("bodyfnt"):
            font = request.form.get("bodyfnt")
            db.execute("UPDATE sessions SET font = :font WHERE element = :element AND session_id = :session_id", font = font, element = "divbody", session_id = session["id"])
        if request.form.get("bodyfntsz"):
            fontsize = request.form.get("bodyfntsz")
            if fontsize.isnumeric() ==  True:
                fontsize = fontsize+ "px"
            db.execute("UPDATE sessions SET fontsize = :fontsize WHERE element = :element AND session_id = :session_id", fontsize = fontsize, element = "divbody", session_id = session["id"])
        if request.form.get("bodytxtclr"):
            textcolor = request.form.get("bodytxtclr")
            db.execute("UPDATE sessions SET textcolor = :textcolor WHERE element = :element AND session_id = :session_id", textcolor = textcolor, element = "divbody", session_id = session["id"])
        if request.form.get("bodyht"):
            height = request.form.get("bodyht")
            db.execute("UPDATE sessions SET height = :height WHERE element = :element AND session_id = :session_id", height = height, element = "divbody", session_id = session["id"])
        if request.form.get("bodywt"):
            width = request.form.get("bodywt")
            db.execute("UPDATE sessions SET width = :width WHERE element = :element AND session_id = :session_id", width = width, element = "divbody", session_id = session["id"])


        if request.form.get("backgroundcolor"):
            bgcolor = request.form.get("backgroundcolor")
            db.execute("UPDATE sessions SET color = :color WHERE element = :element AND session_id = :session_id", color = bgcolor, element = "bckgrd", session_id = session["id"])

        mainbanner = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :mainban", user_id= session["user_id"], session_id = session["id"], mainban = "mainbanner")
        banner1 = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :ban1", user_id = session["user_id"], session_id = session["id"], ban1 = "bannerone")
        bckgrd = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :element", user_id = session["user_id"], session_id = session["id"], element = "bckgrd")
        dbody = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :element", user_id = session["user_id"], session_id = session["id"], element = "divbody")

        return render_template("presets/editpres1.html",color1 = mainbanner[0]["color"], color = banner1[0]["color"], banr1fnt = banner1[0]["font"], mainbnrfnt = mainbanner[0]["font"], banr1fntsz = banner1[0]["fontsize"], mainbnrfntsz = mainbanner[0]["fontsize"], mainbantxtcolor = mainbanner[0]["textcolor"], ban1textclr = banner1[0]["textcolor"], mainbanht = mainbanner[0]["height"], mainbanwt = mainbanner[0]["width"], ban1ht = banner1[0]["height"], ban1wt = banner1[0]["width"], bckgrdcl = bckgrd[0]["color"], bodycolor = dbody[0
]["color"], bodyfnt = dbody[0]["font"], bodyfntsz = dbody[0]["fontsize"], bodytxtclr = dbody[0]["textcolor"], bodyht = dbody[0]["height"], bodywt = dbody[0]["width"])


    else:
        #get
        session_ids = db.execute("SELECT session_id FROM sessions WHERE user_id = :user_id GROUP BY session_id",user_id = session["user_id"])
        session["id"] = len(session_ids)

        if session["id"] == None:
            session["id"] = 0

        #insert default values
        mainban = "mainbanner"
        chocolate = "chocolate"
        ban1 = "bannerone"
        db.execute("INSERT INTO sessions(user_id, session_id,element, color) VALUES(?,?,?,?)", session["user_id"], session["id"],mainban, chocolate)
        db.execute("INSERT INTO sessions(user_id, session_id,element, color, textcolor) VALUES(?,?,?,?,?)", session["user_id"], session["id"],ban1, chocolate, "black")
        db.execute("INSERT INTO sessions(user_id, session_id,element, color) VALUES(?,?,?,?)", session["user_id"], session["id"],"bckgrd", "white")
        db.execute("INSERT INTO sessions(user_id, session_id,element, color, height, width) VALUES(?,?,?,?,?,?)", session["user_id"], session["id"],"divbody", "#E0EEEE", "4.5in", "6in")

        mainbanner = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :mainban", user_id= session["user_id"], session_id = session["id"], mainban = "mainbanner")
        banner1 = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :ban1", user_id = session["user_id"], session_id = session["id"], ban1 = "bannerone")
        bckgrd = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :element", user_id = session["user_id"], session_id = session["id"], element = "bckgrd")
        dbody = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :element", user_id = session["user_id"], session_id = session["id"], element = "divbody")

        return render_template("presets/editpres1.html",color1 = mainbanner[0]["color"], color = banner1[0]["color"], banr1fnt = banner1[0]["font"], mainbnrfnt = mainbanner[0]["font"], banr1fntsz = banner1[0]["fontsize"], mainbnrfntsz = mainbanner[0]["fontsize"], mainbantxtcolor = mainbanner[0]["textcolor"], ban1textclr = banner1[0]["textcolor"], mainbanht = mainbanner[0]["height"], mainbanwt = mainbanner[0]["width"], ban1ht = banner1[0]["height"], ban1wt = banner1[0]["width"], bckgrdcl = bckgrd[0]["color"], bodycolor = dbody[0
]["color"], bodyfnt = dbody[0]["font"], bodyfntsz = dbody[0]["fontsize"], bodytxtclr = dbody[0]["textcolor"], bodyht = dbody[0]["height"], bodywt = dbody[0]["width"])

@app.route("/save", methods=[ "POST"])
def save():
    #check for login
    if session.get("user_id") is None:
        return redirect("/login")
    
    mainbanner = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :mainban", user_id= session["user_id"], session_id = session["id"], mainban = "mainbanner")
    banner1 = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :ban1", user_id = session["user_id"], session_id = session["id"], ban1 = "bannerone")
    bckgrd = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :element", user_id = session["user_id"], session_id = session["id"], element = "bckgrd")
    dbody = db.execute("SELECT * FROM sessions Where user_id = :user_id AND session_id = :session_id AND element = :element", user_id = session["user_id"], session_id = session["id"], element = "divbody")

    return render_template("save.html",color1 = mainbanner[0]["color"], banr1fnt = banner1[0]["font"], mainbnrfnt = mainbanner[0]["font"], mainbnrfntsz = mainbanner[0]["fontsize"], mainbantxtcolor = mainbanner[0]["textcolor"], mainbanht = mainbanner[0]["height"], mainbanwt = mainbanner[0]["width"], color = banner1[0]["color"], banr1fntsz = banner1[0]["fontsize"], ban1textclr = banner1[0]["textcolor"],  ban1ht = banner1[0]["height"], ban1wt = banner1[0]["width"],  bodycolor = dbody[0
    ]["color"], bodyfnt = dbody[0]["font"], bodyfntsz = dbody[0]["fontsize"], bodytxtclr = dbody[0]["textcolor"], bodyht = dbody[0]["height"], bodywt = dbody[0]["width"],banner1 = banner1,bckgrdcl = bckgrd[0]["color"])
    
        
    

def intcheck(x):
    a = False
    for char in x:
        if char.isdigit():
            a = True

    return a