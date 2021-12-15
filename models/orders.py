from app import db
from sqlalchemy.orm import relationship, backref

class OrdersList(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    client_passport_number = db.Column('client_passport_number', db.String(10),
                                       db.ForeignKey('clients_list.passport_number'))
    client = relationship("ClientsList", backref=backref("client", uselist=False))
    rental_time = db.Column('rental_time', db.Integer)
    add_date = db.Column('add_date', db.Date)
    car_number = db.Column('car_number', db.String(8), db.ForeignKey('cars_list.car_number'))
    car = relationship("CarsList", backref=backref("car", uselist=False))

    def __init__(self, id, client, rental_time, add_date, car):
        self.id = id
        self.client = client
        self.rental_time = rental_time
        self.add_date = add_date
        self.car = car

    def __repr__(self):
        return f'car_number: {self.car_number}, rental_time: {self.rental_time}, add_date: {self.add_date}, client_passport_number: {self.client_passport_number}'

    def __gt__(self, other):
        return self.add_date > other.add_date

    def __lt__(self, other):
        return self.add_date < other.add_date