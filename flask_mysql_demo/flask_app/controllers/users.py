from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/edit")
def edit():
    if "user_id" not in session:
        flash("Log in please")
        return redirect("/")

    data = {
        "email":session["email"]
    }
    user = User.get_by_email(data)
    return render_template("edituser.html",user=user)

@app.route("/edituser",methods=["POST"])
def edit_user():
    if "user_id" not in session:
        flash("Log in please")
        return redirect("/")

    if User.validate_update(request.form):
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "id":session["user_id"]
        }
        User.update_user(data)
        session["first_name"] = request.form["first_name"]
        session["email"] = request.form["email"]
        return redirect("/dashboard")
    else:
        return redirect("/edit")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out!")
    return redirect("/")
