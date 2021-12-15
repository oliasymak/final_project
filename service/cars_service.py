from app import db
from models.cars import CarsList
from models.orders import OrdersList


def cars_table():
    '''
    the function returns the clients table
    Parameters:
    :return: clients table
    '''
    return CarsList.query.all()

def car_add(car_description, car_number, rental_cost):
    '''
    The function adds a new item to the client database
    Parameters:
    car_description (string): data from the field car description
    car_number (string): data from the field car number
    rental_cost  (string): data from the field rental cost
    :return: None
    '''
    car = CarsList(car_description, car_number, int(rental_cost), 1)
    db.session.add(car)
    db.session.commit()

def car_edit(ccar_description, ccar_number, rrental_cost, select_car):
    '''
    The function edit an item of the cars table with selected car number,
    edit date in table Orders if it is needed
    Parameters:
    ccar_description (string): data from the field car description
    ccar_number (string): data from the field car number
    rrental_cost  (string): data from the field rental cost
    select_car (string): data from the field selected car
    :return: None
    '''
    car = CarsList('Mercedes', '88888888', 75, 2)
    db.session.add(car)
    OrdersList.query.filter_by(car_number=select_car).update(
        dict(car_number='88888888'))
    CarsList.query.filter_by(car_number=select_car).update(
        dict(car_description=ccar_description, car_number=ccar_number, rental_cost=int(rrental_cost)))
    OrdersList.query.filter_by(car_number='88888888').update(
        dict(car_number=ccar_number))
    CarsList.query.filter(CarsList.car_number == '88888888').delete()
    db.session.commit()

def car_delete_f(ccar_number):
    '''
    The function delete selected car from cars table using car number
    delete order with this car
    :param ccar_number: selected car
    :return: None
    '''
    OrdersList.query.filter(OrdersList.car_number == ccar_number).delete()
    CarsList.query.filter(CarsList.car_number == ccar_number).delete()
    db.session.commit()
