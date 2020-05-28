# Importimg the Libraries
from functools import wraps
import sys
import os
import pyrebase
import json
from flask import *
from flask_mail import Mail, Message
from flask import make_response, send_from_directory, session, request
import requests


############   TEST EMAIL ID   ###############
config = {
    "apiKey": "AIzaSyDKM5jToFhKzJOiEyI13T-7uTZhut-fzVk",
    "authDomain": "test-db319.firebaseapp.com",
    "databaseURL": "https://test-db319.firebaseio.com",
    "projectId": "test-db319",
    "storageBucket": "test-db319.appspot.com",
    "messagingSenderId": "878248691705",
    "appId": "1:878248691705:web:feb670fc0bc47710421f28",
    "measurementId": "G-F07GBFWC5S",
}


# init firebase
firebase = pyrebase.initialize_app(config)
# real time database instance
db = firebase.database()
# auth instance
auth = firebase.auth()
# admin Credentials
admin_email = {"admin1@gmail.com": "password", "admin2@gmail.com": "password"}


# db.child("Names").push({"Name": "Utsav", "Email" : "utsav@gmail.com"})
# db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").update({"Name": "Utsav", "Email" : "maan@gmail.com"})
# users = db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").get()
# print(users.val())
# db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").remove()

# new instance of Flask
app = Flask(__name__)

app.secret_key = os.urandom(24)
#####FOR MAIL#####
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "sample1test.it2@gmail.com"
app.config["MAIL_PASSWORD"] = "youknowhowto"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)
#####FOR MAIL#####

###############dedsec's TEST#################
# post = {
#     "title": "Amadeus",
#     "content": "I am the Greatest Luhar who ever lived",
#     "author": "dedsec995"
# }
# db.child("Posts").push(post)
###############dedsec's TEST#################
# @app.route('/service-worker.js')
# def sw():
#     return app.send_static_file('service-worker.js')


@app.route('/service-worker.js')
def sw():
    response = make_response(
        send_from_directory('static', filename='service-worker.js'))
    # change the content header file
    response.headers['Content-Type'] = 'application/javascript'
    return response


# signup route
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if auth.current_user != None:
#         return redirect(url_for("index"))
#     if request.method == "POST":
#         if request.form["submit"] == "signup":
#             # get the request form data
#             email = request.form["email"]
#             password = request.form["password"]
#             try:
#                 name = request.form["name"]
#                 lastname = request.form["lastname"]
#                 department = request.form["department"]
#                 db.child("Student Name").push(
#                     {
#                         "Name": name,
#                         "Lastname": lastname,
#                         "Email ID": email,
#                         "Password": password,
#                         "Department": department,
#                     }
#                 )
#                 # create the user
#                 auth.create_user_with_email_and_password(email, password)
#                 return redirect("/login")
#             except:
#                 return render_template(
#                     "login.html",
#                     message="The email is already taken, try another one, please",
#                 )
#             # sname = db.child("Student Name").get()
#             # to = sname.val()
#             # return render_template("login.html", t=to.values())
#     return render_template("signup.html", auth=auth)

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('usr', None)
    return redirect(url_for('index'))
# index route
@app.route("/", methods=["GET", "POST"])
def index():
    # auth.current_user = None
    # if auth.current_user != None:
    #     return redirect(url_for("home"))
    try:
        print(session['usr'])
        return redirect(url_for("home"))
    except KeyError:
        allposts = db.child("Posts").get()
        allwebinar = db.child("Webinar").get()
        # if request.method == "POST":
        #     if request.form["submit"] == "Send Message":
        #         try:
        #             name = request.form["name"]
        #             email = request.form["email"]
        #             message = request.form["message"]
        #             msg = Message(
        #                 "Hello {}".format(name.capitalize()),
        #                 sender="sample1test.it2@gmail.com",
        #                 recipients=[email],
        #             )
        #             msg.body = "Hello {}, \n We received your mail regarding a query \n This is your Query :- {} \n \n We hope to resolve your Query as soon as possible".format(
        #                 name.capitalize(), message
        #             )
        #             mail.send(msg)
        #             query = {"email": email, "message": message, "name": name}
        #             db.child("Queries").push(query)
        #             return render_template("thankyou.htm")
        #         except:
        #             return render_template("failed.htm")

        # if allwebinar.val() == None:
        #     return render_template("index.html")
        # else:
        # return render_template("index.html", posts=allposts)
        return render_template("index.html", querys=allwebinar)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        if request.form["submit"] == "login":
            email = request.form["email"]
            password = request.form["password"]
            try:

                # login in the user
                user = auth.sign_in_with_email_and_password(email, password)
                # return user
                user = auth.refresh(user['refreshToken'])
                user_id = user['idToken']
                session['usr'] = user_id
                users = db.child("Student Name").get()
                user1 = users.val()
                # return user1
                for key, values in user1.items():
                    # return values
                    for inkey, invalues in values.items():
                        # return inkey
                        if email in invalues:
                            user_name = values["Name"].upper()
                            dept = values["Department"].upper()
                            try:
                                # news_get = db.child("News Updates").get()
                                return redirect(url_for("home"))
                            except:
                                return "No NEWS FOUND."
                            # return "NO NEWS FOUND"
                            # return redirect(url_for("home"))
                            # render_template(
                            #     "index.html", user_detail=user_name, auth=auth, depart=dept
                            # )
                # return redirect(url_for("home"))
                # render_template("index.html", t=user, auth=auth)
            except:
                # print("Wrong Pass")
                return render_template("login.html", message="Wrong Credentials. Please try again", color="#F66359")
            # print(login)

        elif request.form["submit"] == "pass":
            return redirect(url_for("forgotpass"))
        elif request.form["submit"] == "signup":
            # get the request form data
            email = request.form["email"]
            password = request.form["password"]
            try:
                name = request.form["name"]
                lastname = request.form["lastname"]
                department = request.form["department"]
                location = request.form["location"]
                db.child("Student Name").push(
                    {
                        "Name": name,
                        "Lastname": lastname,
                        "Email ID": email,
                        "Password": password,
                        "Department": department,
                        "Location": location,
                    }
                )
                # create the user
                auth.create_user_with_email_and_password(email, password)
                return render_template("login.html", message="You are Successfully Signed Up", color="#6BBD6E")
            except:
                return render_template(
                    "login.html",
                    message="The email is already taken, try another one, please", color="#FFAA2C"
                )
            # return render_template("forgotpass.html")
    return render_template("login.html")


@app.route("/forgotpass", methods=["GET", "POST"])
def forgotpass():
    if request.method == "POST":
        if request.form["submit"] == "pass":
            email = request.form["email"]
            auth.send_password_reset_email(email)

            # elif request.form["submit"] == "get":
            #     users = db.child("Student Name").get()
            #     a = users.val()
            #     # sub = json.loads(users.val())
            #     print(type(users.val()))
            #     return a
    return render_template("forgotpass.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    # if request.method == "POST":

    users = db.child("Student Name").get()
    allnewsletter = db.child("Newsletter").get()

    # a = {"a": abc, "b": auth.current_user}
    # return a
    user1 = users.val()
    try:
        print(session['usr'])
        abc = auth.get_account_info(session['usr'])
        for key, values in user1.items():
            # return values
            for inkey, invalues in values.items():
                # return inkey
                if abc["users"][0]["email"] in invalues:
                    user_name = values["Name"].upper()
                    dept = values["Department"].upper()
                    first_name = values["Name"]
                    last_name = values["Lastname"]

                    return render_template(
                        "home.html",
                        querys=allnewsletter,
                        first_detail=first_name,
                        last_detail=last_name,
                        email=abc["users"][0]["email"],
                        depart=dept
                    )
    except KeyError:
        return redirect(url_for("index"))


# Webinar

@app.route("/webinar", methods=["GET", "POST"])
def webinar():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":
    try:
        print(session['usr'])
        allwebinar = db.child("Webinar").get()
        if allwebinar.val() == None:
            return render_template("webinar.html")
        else:
            return render_template("webinar.html", querys=allwebinar)

    except KeyError:
        return redirect(url_for("index"))


@app.route("/newsf", methods=["GET", "POST"])
def newsf():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":
    # try:

    try:
        print(session['usr'])

        users = db.child("Student Name").get()
        user = users.val()
        abc = auth.get_account_info(session['usr'])
        for key, values in user.items():
            # return values
            for inkey, invalues in values.items():
                # return inkey
                if abc["users"][0]["email"] in invalues:
                    user_name = values["Name"].upper()
                    first_name = values["Name"]
                    last_name = values["Lastname"]
                    dept = values["Department"].upper()
                    try:
                        news_get = db.child("News Updates").get()
                        return render_template("news.html", allnews=news_get, first_detail=first_name, last_detail=last_name, depart=dept)
                    except:
                        return "No NEWS FOUND."

    except KeyError:
        return redirect(url_for("index"))


@app.route("/ucoeclan", methods=["GET", "POST"])
def ucoeclan():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    try:
        print(session['usr'])
        return render_template("ucoeclan.html")
    except KeyError:
        return redirect(url_for("index"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":

    users = db.child("Student Name").get()
    user = users.val()
    try:
        print(session['usr'])
        abc = auth.get_account_info(session['usr'])
        for key, values in user.items():
            # return values
            for inkey, invalues in values.items():
                # return inkey
                if abc["users"][0]["email"] in invalues:
                    user_name = values["Name"].upper()
                    first_name = values["Name"]
                    location = values["Location"]
                    last_name = values["Lastname"]
                    dept = values["Department"].upper()

                    return render_template(
                        "profile.html",
                        first_detail=first_name,
                        last_detail=last_name,
                        email=abc["users"][0]["email"],
                        loc=location,
                        depart=dept
                    )
    except KeyError:
        return redirect(url_for("index"))


@app.route("/ucoeclan/<dept>", methods=["GET", "POST"])
def ucoeclan1(dept):
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":

    allnewsletter = db.child("Newsletter").get()
    users = db.child("Student Name").get()
    user = users.val()
    try:
        print(session['usr'])
        abc = auth.get_account_info(session['usr'])
        if dept != None:
            for key, values in user.items():
                # return values
                for inkey, invalues in values.items():
                    # return inkey
                    if abc["users"][0]["email"] in invalues:
                        user_name = values["Name"].upper()
                        # dept = values["Department"].upper()
                        first_name = values["Name"]
                        last_name = values["Lastname"]
                        return render_template("depart.html",  first_detail=first_name,
                                               last_detail=last_name, querys=allnewsletter, depart=dept)
    except KeyError:
        return redirect(url_for("index"))


@app.route("/news", methods=["GET", "POST"])
def news():

    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":

    users = db.child("Student Name").get()
    user = users.val()
    try:
        print(session['usr'])
        abc = auth.get_account_info(session['usr'])
        for key, values in user.items():
            # return values
            for inkey, invalues in values.items():
                # return inkey
                if abc["users"][0]["email"] in invalues:
                    user_name = values["Name"].upper()
                    dept = values["Department"].upper()
                    first_name = values["Name"]
                    last_name = values["Lastname"]
                    try:
                        news_get = db.child("News Updates").get()

                        return render_template(
                            "student.html",
                            allnews=news_get,
                            user_detail=user_name,
                            first_detail=first_name,
                            last_detail=last_name, depart=dept
                        )

                    except:
                        return "No NEWS FOUND."
    except KeyError:
        return redirect(url_for("index"))

# Comps
@app.route("/comps", methods=["GET", "POST"])
def comps():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":

    allnewsletter = db.child("Newsletter").get()
    if allnewsletter.val() == None:
        return render_template("comps.html")
    else:
        return render_template("comps.html", querys=allnewsletter)


@app.route("/courses", methods=["GET", "POST"])
def courses():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":

    allquery = db.child("Courses").get()
    users = db.child("Student Name").get()
    user = users.val()
    try:
        print(session['usr'])
        abc = auth.get_account_info(session['usr'])
        if allquery.val() == None:
            return render_template("courses.html")
        else:
            for key, values in user.items():
                # return values
                for inkey, invalues in values.items():
                    # return inkey
                    if abc["users"][0]["email"] in invalues:
                        user_name = values["Name"].upper()
                        dept = values["Department"].upper()
                        first_name = values["Name"]
                        last_name = values["Lastname"]
                        return render_template("courses.html", first_detail=first_name,
                                               last_detail=last_name, querys=allquery,  depart=dept)
    except KeyError:
        return redirect(url_for("index"))


@app.route("/courses1", methods=["GET", "POST"])
def courses1():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":

    allquery = db.child("Courses").get()
    users = db.child("Student Name").get()
    user = users.val()
    if allquery.val() == None:
        return render_template("onlinecourse.html")
    else:
        return render_template("onlinecourse.html", querys=allquery)


@app.route("/contact1", methods=["GET", "POST"])
def contact1():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":
    if request.method == "POST":
        if request.form["submit"] == "Send Message":
            try:
                name = request.form["name"]
                email = request.form["email"]
                message = request.form["message"]
                msg = Message(
                    "Hello {}".format(name.capitalize()),
                    sender="sample1test.it2@gmail.com",
                    recipients=[email],
                )
                msg.body = "Hello {}, \n We received your mail regarding a query \n This is your Query :- {} \n \n We hope to resolve your Query as soon as possible".format(
                    name.capitalize(), message)
                mail.send(msg)
                query = {"email": email,
                         "message": message, "name": name}
                db.child("Queries").push(query)
                return redirect(url_for("thank"))
            except:
                return redirect(url_for("fail"))
    return render_template("contact1.html")


@app.route("/thank", methods=["GET", "POST"])
def thank():
    render_template("thankyou.htm")


@app.route("/fail", methods=["GET", "POST"])
def fail():
    render_template("failed.htm")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    # if auth.current_user == None:
    #     return redirect(url_for("login"))
    # if request.method == "POST":

    users = db.child("Student Name").get()
    user = users.val()
    if request.method == "POST":
        if request.form["submit"] == "Send Message":
            try:
                name = request.form["name"]
                email = request.form["email"]
                message = request.form["message"]
                msg = Message(
                    "Hello {}".format(name.capitalize()),
                    sender="sample1test.it2@gmail.com",
                    recipients=[email],
                )
                msg.body = "Hello {}, \n We received your mail regarding a query \n This is your Query :- {} \n \n We hope to resolve your Query as soon as possible".format(
                    name.capitalize(), message)
                mail.send(msg)
                query = {"email": email,
                         "message": message, "name": name}
                db.child("Queries").push(query)
                return redirect(url_for("thank"))
            except:
                return redirect(url_for("fail"))
    try:
        print(session['usr'])
        abc = auth.get_account_info(session['usr'])
        for key, values in user.items():
            # return values
            for inkey, invalues in values.items():
                # return inkey
                if abc["users"][0]["email"] in invalues:
                    user_name = values["Name"].upper()
                    dept = values["Department"].upper()
                    first_name = values["Name"]
                    last_name = values["Lastname"]
                    return render_template("contact.html", first_detail=first_name,
                                           last_detail=last_name,  depart=dept)
    except KeyError:
        return redirect(url_for("index"))


@app.route("/events", methods=["GET", "POST"])
def events():
    try:
        print(session['usr'])
        return render_template("events.html", )
    except KeyError:
        return redirect(url_for("index"))


@app.route("/location", methods=["GET", "POST"])
def location():
    allquery = db.child("Student Name").get()
    if allquery.val() == None:
        return render_template("location.html")
    else:
        return render_template("location.html", querys=allquery, )


@app.route("/offline", methods=["GET", "POST"])
def offline():
    return render_template("offline.html")


@app.route("/admin.html", methods=["GET", "POST"])
def admin():
    allquery = db.child("Queries").get()
    if request.method == "POST":
        if request.form["submit"] == "addNews":
            headline = request.form["headline"]
            story = request.form["story"]
            imagelink = request.form["imagelink"]
            imagelink = imagelink.replace("open", "uc")
            allnews = {
                "headline": headline,
                "story": story,
                "imagelink": imagelink,
            }
            db.child("News Updates").push(allnews)

        if request.form["submit"] == "addWebinar":
            link = request.form["link"]
            professor = request.form["professor"]
            date = request.form["date"]
            domain = request.form["domain"]
            webinar = {
                "link": link,
                "professor": professor,
                "date": date,
                "domain": domain,
            }
            db.child("Webinar").push(webinar)

        if request.form["submit"] == "addNewsletter":
            link = request.form["link"]
            linkcoverpage = request.form["linkcoverpage"]
            linkcoverpage = linkcoverpage.replace("open", "uc")
            title = request.form["title"]
            issue = request.form["issue"]
            domain = request.form["domain"]
            newsletter = {
                "link": link,
                "linkcoverpage": linkcoverpage,
                "title": title,
                "issue": issue,
                "domain": domain,
            }
            db.child("Newsletter").push(newsletter)

        if request.form["submit"] == "addCourses":
            name = request.form["name"]
            link = request.form["link"]
            description = request.form["description"]
            courses = {
                "name": name,
                "link": link,
                "description": description,
            }
            db.child("Courses").push(courses)

        # elif request.form["submit"] == "news":
        #     try:
        #         news_get = db.child("News Updates").get()
        #         return render_template("news.html", news=news_get.val())
        #     except:
        #         return "NO NEWS FOUND"
        # news = news_get.val()
    if allquery.val() == None:
        return render_template("admin.html")
    else:
        return render_template("admin.html", querys=allquery)


@app.route("/adminlogin.html", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        if request.form["submit"] == "adminlogin":
            email = request.form["email"]
            password = request.form["password"]
            try:
                admin_email[email] == password
                try:
                    login = auth.sign_in_with_email_and_password(
                        email, password)
                    return render_template("admin.html")
                except:
                    return "Errorrrr Loading page please try again Later......"
            except:
                return "Wrong Email or Password"

            # print(login)

        elif request.form["submit"] == "home":
            return render_template("index.html")
    return render_template("adminlogin.html")


if __name__ == "__main__":
    app.run(debug=True)
