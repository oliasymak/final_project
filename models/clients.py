from app import db
import datetime
class ClientsList(db.Model):
    __table__name = 'clients_list'

    first_name = db.Column('first_name', db.String(40))
    last_name = db.Column('last_name', db.String(40))
    passport_number = db.Column('passport_number', db.String(10), primary_key=True)
    add_date = db.Column('add_date', db.Date)
    number_of_orders_clients = db.Column('number_of_orders_clients', db.Integer)

    def __init__(self, first_name, last_name, passport_number, add_date, number_of_orders_clients):
        self.first_name = first_name
        self.last_name = last_name
        self.passport_number = passport_number
        self.add_date = add_date
        self.number_of_orders_clients = number_of_orders_clients

    def __repr__(self):
        return f'first_name: {self.first_name},last_name: {self.last_name},passport_number: {self.passport_number},add_date: {self.add_date},number_of_orders_clients: {self.number_of_orders_clients}'

    def __gt__(self, other):
        return self.add_date > other.add_date

    def __lt__(self, other):
        return self.add_date < other.add_date