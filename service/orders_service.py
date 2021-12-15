from app import db
from models.cars import CarsList
from models.orders import OrdersList
from models.clients import ClientsList


def orders_table():
    '''
    the function returns the orders table
    Parameters:
    :return: orders table
    '''
    return db.session.query(OrdersList).order_by(OrdersList.id)

def order_add(ccar_number, cpassport_number, rental_time, add_date):
    '''
    The function adds a new item to the order database,
    updates the number of orders in the table customers and machines
    Parameters:
    cpassport_number (string): data from the field passport number
    ccar_number (string): data from the field car number
    rental_time (int): data from the field rental time
    add_date (string): data from the field add date
    :return: None
    '''
    count_rows = db.session.query(OrdersList).count()
    car = CarsList.query.filter_by(car_number=ccar_number).first()
    client = ClientsList.query.filter_by(passport_number=cpassport_number).first()
    order = OrdersList(count_rows + 1, client, int(rental_time), add_date, car)
    db.session.add(order)
    db.session.commit()
    OrdersList.query.filter_by(car_number=None).update(dict(car_number=ccar_number))
    OrdersList.query.filter_by(client_passport_number=None).update(dict(client_passport_number=cpassport_number))
    car = CarsList.query.filter_by(car_number=ccar_number)
    client = ClientsList.query.filter_by(passport_number=cpassport_number)
    car_number_orders = car[0].number_of_orders_cars + 1
    client_number_orders = client[0].number_of_orders_clients + 1
    CarsList.query.filter_by(car_number=ccar_number).update(
        dict(number_of_orders_cars=car_number_orders))
    ClientsList.query.filter_by(passport_number=cpassport_number).update(
        dict(number_of_orders_clients=client_number_orders))
    db.session.flush()
    db.session.commit()


def order_edit(ppassport_number, ccar_number, rrental_time, aadd_date, select_order):
    '''
    The function edit an item of the order table with selected id,
    Edit numbers of orders in car and client table
    Parameters:
    ppassport_number (string): data from the field passport number
    ccar_namber (string): data from the field car number
    rrental_time  (string): data from the field rental cost
    aadd_date (string): data from the field add date
    select_order (string): data from the field selected order
    :return: None
    '''
    select_order_client = OrdersList.query.filter_by(id=select_order)
    select_client_passport = select_order_client[0].client_passport_number
    client = ClientsList.query.filter_by(passport_number=select_client_passport)
    number_orders = client[0].number_of_orders_clients
    number_orders = number_orders - 1
    ClientsList.query.filter_by(passport_number=select_client_passport).update(
        dict(number_of_orders_clients=number_orders))

    select_order_car = OrdersList.query.filter_by(id=select_order)
    select_car_number = select_order_car[0].car_number
    car = CarsList.query.filter_by(car_number=select_car_number)
    number_carorders = car[0].number_of_orders_cars
    number_carorders = number_carorders - 1
    CarsList.query.filter_by(car_number=select_car_number).update(
        dict(number_of_orders_cars=number_carorders))

    OrdersList.query.filter_by(id=select_order).update(
        dict(car_number=ccar_number, client_passport_number=ppassport_number, rental_time=int(rrental_time),
             add_date=aadd_date))

    client1 = ClientsList.query.filter_by(passport_number=ppassport_number)
    number_orders1 = client1[0].number_of_orders_clients
    number_orders1 = number_orders1 + 1
    ClientsList.query.filter_by(passport_number=ppassport_number).update(
        dict(number_of_orders_clients=number_orders1))

    car1 = CarsList.query.filter_by(car_number=ccar_number)
    number_orders2 = car1[0].number_of_orders_cars
    number_orders2 = number_orders2 + 1
    CarsList.query.filter_by(car_number=ccar_number).update(
        dict(number_of_orders_cars=number_orders2))

    db.session.flush()
    db.session.commit()


def order_delete_f(order_id):
    '''
    The function delete selected order from orders table using id
    :param order_id: selected order
    :return: None
    '''

    select_order_car = OrdersList.query.filter_by(id=int(order_id))
    select_car_number = select_order_car[0].car_number
    car = CarsList.query.filter_by(car_number=select_car_number)
    number_carorders = car[0].number_of_orders_cars
    number_carorders = number_carorders - 1
    CarsList.query.filter_by(car_number=select_car_number).update(
        dict(number_of_orders_cars=number_carorders))
    select_order_client = OrdersList.query.filter_by(id=int(order_id))
    select_client_passport = select_order_client[0].client_passport_number
    client = ClientsList.query.filter_by(passport_number=select_client_passport)
    number_orders = client[0].number_of_orders_clients
    number_orders = number_orders - 1
    ClientsList.query.filter_by(passport_number=select_client_passport).update(
        dict(number_of_orders_clients=number_orders))
    OrdersList.query.filter(OrdersList.id == int(order_id)).delete()
    db.session.commit()