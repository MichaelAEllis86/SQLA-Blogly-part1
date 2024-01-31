from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///blogly_db'
app.config['SQLALCHEMY_ECHO']= True
app.config['SECRET_KEY']="oh-so-secret"
debug=DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def show_base():
    """show base/home page"""
    return render_template("base.html")

@app.route("/users")
def show_user_list_page():
    """show all the pets in our db"""
    users=User.query.all()
    return render_template("users.html", users=users )

@app.route("/users/new")
def show_new_user_form_page():
    return render_template("userform.html")

@app.route("/users/new", methods=['POST'] )
def handle_new_user_form():
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]
    print(f"the form data is first name={first_name} last_name={last_name} image url={image_url}")
    new_user=User(first_name=first_name, last_name=last_name, image_url=image_url)
    print(f"the new user is {new_user}")
    db.session.add(new_user)
    db.session.commit()
    flash("new user created!!")
    flash(f"your new user is {new_user.first_name}{new_user.last_name} with a user id of {new_user.id}", "success")
    return redirect("/users")

@app.route("/users/<user_id>")
def show_user_details(user_id):
    user=User.query.get(user_id)
    print("the user is", user)
    print(f"the user_id is {user_id}")
    print(f"the user_id type is {type(user_id)}")
    return render_template("userdetail.html", user=user, user_id=user_id)

@app.route("/users/<user_id>/edit")
def show_user_edit(user_id):
    user=User.query.get(user_id)
    return render_template("usereditform.html", user=user,user_id=user_id)

@app.route("/users/<user_id>/edit", methods=['POST'])
def handle_user_edit(user_id):
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]
    user=User.query.get(int(user_id))
    print(f"this is the intial user{user}")
    user.first_name=first_name
    user.last_name=last_name
    user.image_url=image_url
    print(f"this is user now {user}")
    db.session.add(user)
    db.session.commit()
    flash("user edited!!")
    flash(f"your user is now {user.first_name}{user.last_name} with a user id of {user.id}", "success")
    return redirect("/users")

@app.route("/users/<user_id>/delete", methods=['POST'])
def handle_user_delete(user_id):
    print(f" the initial user_id is {user_id} and it's type is {type(user_id)}")
    integer_user_id=int(user_id)
    user=User.query.get(int(user_id))
    User.query.filter_by(id=integer_user_id).delete()
    db.session.commit()
    flash("user deleted!!")
    flash(f"the previous user of {user.first_name}{user.last_name} with a user id of {user.id} is now deleted" "success")
    return redirect("/users")




