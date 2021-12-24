from app import db
from models.clients import ClientsList
from models.cars import CarsList
from models.orders import OrdersList
from datetime import date

def fill_database():
    '''
    in this function,  first completely clear the database and populate it again,
     add new elements to database
    Parameters:
    client1, client2, client3, client4, client5: elements of class ClientsList
    car1, car2, car3, car4, car5: elements of class CarsList
    order1, order2, order3, order4, order5, order6: elements of class OrdersList

    '''
    db.drop_all()
    db.create_all()
    client1 = ClientsList('Ірина', 'Дмитрасевич', 'ab2413', date(2021, 11, 22), 2)
    client2 = ClientsList('Дмитро', 'Гнатенко', 'ac4123', date(2021, 10, 20), 1)
    client3 = ClientsList('Ігор', 'Петриляк', 'ac5678', date(2021, 11, 15), 1)
    client4 = ClientsList('Ольга', 'Юрків', 'af3553', date(2021, 9, 8), 1)
    client5 = ClientsList('Назар', 'Сохан', 'ab3421', date(2021, 10, 30), 1)

    car1 = CarsList('bmw', 'ВС3457НО', 85, 1)
    car2 = CarsList('Audi', 'ВС8742ОВ', 80, 1)
    car3 = CarsList('Renault', 'ВС8771КК', 70, 1)
    car4 = CarsList('Opel', 'ВС8734АА', 60, 1)
    car5 = CarsList('Mercedes', 'ВС9812ММ', 75, 2)

    order1 = OrdersList(1, client1, 2, date(2021, 11, 22), car2)
    order2 = OrdersList(2, client3, 1, date(2021, 11, 15), car3)
    order3 = OrdersList(3, client5, 3, date(2021, 10, 30), car1)
    order4 = OrdersList(4, client4, 2, date(2021, 9, 8), car4)
    order5 = OrdersList(5, client2, 1, date(2021, 10, 20), car5)
    order6 = OrdersList(6, client1, 3, date(2021, 12, 1), car5)

    db.session.add(client1)
    db.session.add(client2)
    db.session.add(client3)
    db.session.add(client4)
    db.session.add(client5)

    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)
    db.session.add(car4)
    db.session.add(car5)

    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)
    db.session.add(order4)
    db.session.add(order5)
    db.session.add(order6)

    db.session.commit()

fill_database()
