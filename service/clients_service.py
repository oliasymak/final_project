from app import db
from datetime import date
from datetime import datetime
from models.orders import OrdersList
from models.clients import ClientsList


def clients_table():
    '''
        the function returns the clients table
        Parameters:
        :return: clients table
    '''
    return ClientsList.query.all()


def client_add(first_name, last_name, passport_number, add_date):
    '''
    The function adds a new item to the client database
    Parameters:
    first_name (string): data from the field first name
    last_name (string): data from the field last name
    passport_number  (int): data from the field passport number
    add_date (string): data from the field add date
    :return: None
    '''
    add_date1 = datetime.strptime(add_date, "%Y-%m-%d")
    client = ClientsList(first_name, last_name, passport_number, add_date1, 1)
    db.session.add(client)
    db.session.commit()


def client_edit(ffirst_name, llast_name, ppassport_number, aadd_date, select_client):
    '''
    The function edit an item of the clients table with selected passport number,
    edit date in table Orders if it is needed

    Parameters:
    ffirst_name (string): data from the field first name
    llast_name (string): data from the field last name
    ppassport_number  (string): data from the field passport number
    aadd_date (string): data from the field add date
    select_client (string): data from the field selected client
    :return: None
    '''
    add_date1 = datetime.strptime(aadd_date, "%Y-%m-%d")
    client = ClientsList('Назар', 'Сохан', '888888', date(2021, 10, 30), 1)
    db.session.add(client)
    OrdersList.query.filter_by(client_passport_number=select_client).update(
        dict(client_passport_number='888888'))
    ClientsList.query.filter_by(passport_number=select_client).update(
        dict(first_name=ffirst_name, last_name=llast_name, passport_number=ppassport_number, add_date=add_date1))
    OrdersList.query.filter_by(client_passport_number='888888').update(
        dict(client_passport_number=ppassport_number))
    ClientsList.query.filter(ClientsList.passport_number == '888888').delete()
    db.session.commit()


def client_delete_f(ppassport_number):
    '''
    The function delete selected client from clients table using passport number
    delete order with this client
    :param ppassport_number: selected client
    :return: None
    '''
    OrdersList.query.filter(OrdersList.client_passport_number == ppassport_number).delete()
    ClientsList.query.filter(ClientsList.passport_number == ppassport_number).delete()
    db.session.commit()
