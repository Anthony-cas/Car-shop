from flask_app import app
from flask import render_template, session, url_for, redirect, request
from flask_app.models import car
from flask import flash


@app.route("/cars/create")
def add_car():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    return render_template("add_car.html")

@app.route("/car/process", methods=["POST"])
def create_car():

    if not car.Car.is_valid(request.form):
        return redirect(url_for("add_car"))
    else:
        data = {
            "id" : id,
            "price" : request.form["price"],
            "model" : request.form["model"],
            "make" : request.form["make"],
            "year" : request.form["year"],
            "description" : request.form["description"],
            "user_id" : int(session["logged_in"])
        }
        car.Car.create(data)
        return redirect("/dashboard")

@app.route("/cars/edit/<int:id>")
def edit_car(id):
    one_car = car.Car.get_one_with_user({"id" : id})
    return render_template("edit_car.html", one_car = one_car)


@app.route("/car/update/<int:id>", methods=["POST"])
def update_car(id):
    if not car.Car.is_valid(request.form):
        return redirect(url_for("edit_car"))
    else:
        data = {
            "id" : id,
            "price" : request.form["price"],
            "model" : request.form["model"],
            "make" : request.form["make"],
            "year" : request.form["year"],
            "description" : request.form["description"],
            "user_id" : int(session["logged_in"])
        }
        car.Car.update(data)
    return redirect("/dashboard")
    

@app.route("/car/<int:id>")
def one_car(id):
    user_id = int(session["logged_in"])
    car_in_db = car.Car.get_one_with_user({"id": id})
    return render_template("one_car.html", one_car = car_in_db, user_id = user_id)

@app.route("/cars/delete/<int:id>")
def destroy(id):
    car.Car.destroy({"id": id})
    return redirect(url_for("dashboard"))