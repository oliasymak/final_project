from app import db

class CarsList(db.Model):
    car_description = db.Column('car_description', db.String(20))
    car_number = db.Column('car_number', db.String(8), primary_key=True)
    rental_cost = db.Column('rental_cost', db.Numeric)
    number_of_orders_cars = db.Column('number_of_orders_cars', db.Integer)

    def __init__(self, car_description, car_number, rental_cost, number_of_orders_cars):
        self.car_description = car_description
        self.car_number = car_number
        self.rental_cost = rental_cost
        self.number_of_orders_cars = number_of_orders_cars

    def __repr__(self):
        return f'cars_description: {self.car_description}, car_number: {self.car_number},rental_cost: {self.rental_cost},number_of_orders_cars: {self.number_of_orders_cars}'

    def __gt__(self, other):
        return self.rental_cost > other.rental_cost

    def __lt__(self, other):
        return self.rental_cost < other.rental_cost