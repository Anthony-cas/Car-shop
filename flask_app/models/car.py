from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Car:
    db = "exam_prep"
    def __init__(self, data):
        self.id = data["id"]
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.seller = None


    @classmethod
    def get_all(cls):
        query =  "SELECT * FROM cars;"
        results = connectToMySQL(cls.db).query_db(query)
        all_cars = []
        for row in results:
            all_cars.append(cls(row))
        return all_cars


    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO cars(price, model, make, year, description, user_id) VALUES (%(price)s,%(model)s,%(make)s,%(year)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users on users.id = cars.user_id WHERE cars.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        row = results[0]
        one_car = cls(row)
        user_data = {
            "id" : row["id"],
            "first_name" : row["first_name"],
            "last_name" : row["last_name"],
            "username" : row["username"],
            "email" : row["email"],
            "password" : row["password"],
            "created_at" : row["created_at"],
            "updated_at" : row["updated_at"]
        }
        one_car.creator = user.User(user_data)
        return one_car

        


    
    @classmethod
    def update (cls, data):
        query = "Update cars SET price=%(price)s, model=%(model)s, make=%(make)s, year=%(year)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def get_all_with_seller(cls):
        query = "SELECT cars.*, users.first_name, users.last_name FROM cars LEFT JOIN users ON cars.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        cars = [cls(row) for row in results]
        return cars

    
    @staticmethod
    def is_valid(car):
        is_valid = True
        if len(car["price"]) < 1:
            flash("car price must be at least 1 characters")
            is_valid = False
        if len(car["model"]) < 1:
            flash("car model must be at least 1 characters")
            is_valid = False
        if len(car["make"]) < 1:
            flash("car make must be at least 1 characters")
            is_valid = False
        if len(car["year"]) < 1:
            flash("year must be at least 1 characters")
            is_valid = False
        if len(car["description"]) <10:
            flash("car description must be at least 10 characters")
            is_valid = False
        return is_valid

