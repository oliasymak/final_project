from app import db
from models.clients import ClientsList
from models.cars import CarsList
from models.orders import OrdersList
from datetime import date, timedelta
import random


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
    first_names_list = ['Ірина', 'Дмитро', 'Ігор', 'Ольга', 'Назар', 'Анастасія', 'Давид', 'Олег',
                        'Соломія', 'Андрій', 'Надія', 'Наталія', 'Федір', 'Григорій', 'Петро']
    last_names_list = ['Дмитрасевич', 'Гнатенко', 'Петриляк', 'Юрків', 'Сохан', 'Юськів', 'Соколівський',
                       'Янів', 'Янківська', 'Ковалишин', 'Фендак', 'Гончаренко', 'Степаненко', 'Сидоренко',
                       'Гнатюк', ]
    passport_numbers_list = ['ab2413', 'ac4123', 'ac5678', 'af3553', 'ab3421', 'ab2715',
                             'ab1314', 'ac1314', 'ac9876', 'ab9876', 'af5467', 'ak8976',
                             'ak1234', 'ac7777', 'ab0909', ]

    test_date1, test_date2 = date(2021, 2, 5), date(2021, 10, 1)
    K = 15
    dates = [test_date1]
    while test_date1 != test_date2:
        test_date1 += timedelta(days=1)
        dates.append(test_date1)
    dates_list = random.choices(dates, k=K)
    clients = []
    for i in range(len(passport_numbers_list)):
        clients.append(ClientsList(first_names_list[i], last_names_list[i], passport_numbers_list[i], dates_list[i], 0))

    car_description_list = ['bmw', 'Audi', 'Renault', 'Opel', 'Mercedes', 'Ford', 'Volkswagen', 'Renault',
                            'Chevrolet', 'Mazda', 'Lexus', 'Peugeot', 'Toyota', 'Skoda', 'Suzuki', 'SEAT',
                            'Porche', 'Citroen', 'Mitsubishi', 'Dacia']
    car_numbers_list = ['ВС3457НО', 'ВС8742ОВ', 'ВС8771КК', 'ВС8734АА', 'ВС9812ММ', 'ВС6574РР', 'ВС7383КА',
                        'ВС1265КО', 'ВС9778ММ', 'ВС9270ММ', 'ВС5673ЛК', 'ВС7462ОО', 'ВС2743ЛК', 'ВС4526МС',
                        'ВС1234МС', 'ВС4983КК', 'ВС4447МС', 'ВС1252МК', 'ВС4988КО', 'ВС7772АР']
    price_list = [85, 80, 70, 60, 75, 100, 110, 65, 110, 115, 130, 80, 90, 75, 95, 75, 150, 70, 85, 60]
    cars_list = []
    for i in range(len(car_numbers_list)):
        cars_list.append(CarsList(car_description_list[i], car_numbers_list[i], price_list[i], 0))


    orders = []
    for i in range(100):
        orders.append(OrdersList(i + 1, random.choice(clients), random.randint(1, 10), random.choice(dates_list),
                                 random.choice(cars_list)))
    for i in orders:
        db.session.add(i)
    number_of_orders_list = []
    for i in car_numbers_list:
        number_of_orders_list.append(OrdersList.query.filter_by(car_number=i).count())
    number_of_orders_list1 = []
    for i in passport_numbers_list:
        number_of_orders_list1.append(OrdersList.query.filter_by(client_passport_number=i).count())
    print(number_of_orders_list1)
    for i in range(len(car_numbers_list)):
        CarsList.query.filter_by(car_number=car_numbers_list[i]).update(
            dict(number_of_orders_cars=number_of_orders_list[i]))
    for i in range(len(passport_numbers_list)):
        ClientsList.query.filter_by(passport_number=passport_numbers_list[i]).update(
            dict(number_of_orders_clients=number_of_orders_list1[i]))
    db.session.commit()


fill_database()
