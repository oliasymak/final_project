from app import app
from app import db
from flask import render_template, request
from flask import redirect
from flask import url_for
from service.cars_service import *


@app.route('/cars_list', methods=["GET"])
def cars_list():
    '''
    The functions returns the page with table CarsList
    Parameters:
    rows (class): table CarsList
    :return: prototype_cars_list_general.html
    '''
    rows = cars_table()
    if request.method == "GET":
        return render_template("prototype_cars_list_general.html", rows=rows)
    return redirect(url_for('cars_list'))


@app.route('/add_car', methods=["GET", "POST"])
def add_car():
    '''
    The function returns the layout of the add car page
    :return: prototype_add_car.html
    '''
    if request.method == "GET":
        return render_template("prototype_add_car.html")
    return redirect(url_for('add_car'))


@app.route('/cars_list_add', methods=["GET", "POST"])
def cars_list_add():
    '''
    The function adds a new item to the client database,
    returns a page with an updated client table
    if entered data is not correct, function return page with error
    Parameters:
    car_description (string): data from the field car description
    car_number (string): data from the field car number
    rental_cost  (string): data from the field rental cost
    rows (class): table of cars
    :return: prototype_cars_list_general.html
    '''
    if request.method == "POST":
        car_description = request.form.get('cname')
        car_number = request.form.get('cdes').strip()
        rental_cost = request.form.get('rtime').strip()
    if car_description == '' or car_number == '' or rental_cost == '':
        return render_template("prototype_data_not_correct.html")
    if car_description.isdigit() or car_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    if not rental_cost.isdigit():
        return render_template("prototype_data_not_correct.html")
    if len(car_number) > 8:
        return render_template("prototype_data_not_correct.html")
    car_add(car_description, car_number, rental_cost)
    rows = cars_table()
    return render_template("prototype_cars_list_general.html", rows=rows)






@app.route('/edit_car', methods=["GET", "POST"])
def edit_car():
    '''
    The function returns the layout of the edit car page
    :return: prototype_edit_car.html
    '''
    if request.method == "GET":
        return render_template("prototype_edit_car.html")
    return redirect(url_for('edit_car'))


@app.route('/cars_list_edit', methods=["GET", "POST"])
def cars_list_edit():
    '''
        The function edit an item of the cars table with selected car number,
        returns a page with an updated cars table,
        edit date in table Orders if it is needed
        if entered data is not correct, function return page with error
        Parameters:
        ccar_description (string): data from the field car description
        ccar_number (string): data from the field car number
        rrental_cost  (string): data from the field rental cost
        select_car (string): data from the field selected car
        rows (class): table of cars
        :return: prototype_cars_list_general.html
    '''
    if request.method == "POST":
        ccar_description = request.form.get('cname').strip()
        ccar_number = request.form.get('cdes').strip()
        rrental_cost = request.form.get('rtime').strip()
        select_car = request.form.get('select_car').strip()
    if ccar_description == '' or ccar_number == '' or rrental_cost == '':
        return render_template("prototype_data_not_correct.html")
    if ccar_description.isdigit() or ccar_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    if not rrental_cost.isdigit():
        return render_template("prototype_data_not_correct.html")
    if len(ccar_number) > 8:
        return render_template("prototype_data_not_correct.html")
    if CarsList.query.get(select_car) == None:
        return render_template("prototype_data_not_correct.html")
    car_edit(ccar_description, ccar_number, rrental_cost, select_car)
    # rows = db.session.query(CarsList)
    rows = cars_table()
    return render_template("prototype_cars_list_general.html", rows=rows)






@app.route('/refresh_сar', methods=["GET", "POST"])
def refresh_car():
    '''
    The function filters cars in the range of entered dates,
    return the table of cars with this elements
    If rental cost from is empty the function return the page with all elements by some rental cost
    If rental cost by is empty the function return the page with all elements from some rental cost till the end
    If rental cost by and from is empty the function return the page with all elements
    Parameters:
    rental_from (string): data from field rental from
    rental_by (string): data from field by
    :return:prototype_cars_list_general.html
    '''
    if request.method == "POST":
        rental_from = request.form.get('number1')
        rental_by = request.form.get('number2')

    if rental_from == '' and rental_by == '':
        rows = cars_table()
        return render_template("prototype_cars_list_general.html", rows=rows)
    if rental_from == '':
        from1 = db.session.query(CarsList).order_by(CarsList.rental_cost)
        rows = db.session.query(CarsList).filter(CarsList.rental_cost.between(from1[0].rental_cost, int(rental_by)))
        return render_template("prototype_cars_list_general.html", rows=rows)
    if rental_by == '':
        from1 = db.session.query(CarsList).order_by(CarsList.rental_cost)
        rows = db.session.query(CarsList).filter(CarsList.rental_cost.between(int(rental_from), from1[-1].rental_cost))
        return render_template("prototype_cars_list_general.html", rows=rows)
    rows = db.session.query(CarsList).filter(CarsList.rental_cost.between(int(rental_from), int(rental_by)))
    return render_template("prototype_cars_list_general.html", rows=rows)


@app.route('/car_delete', methods=["GET", "POST"])
def car_delete():
    '''
    The function delete car from cars table using car number,
    delete order with this car
    return page with updated cars table
    if entered data is not correct, function return page with error
    Parameters:
    ccar_number (string): data from field car number
    rows: cars table
    :return: prototype_cars_list_general.html
    '''
    if request.method == "POST":
        ccar_number = request.form.get('cdes').strip()
    if CarsList.query.get(ccar_number) == None:
        return render_template("prototype_data_not_correct.html")
    if ccar_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    car_delete_f(ccar_number)
    rows = cars_table()
    return render_template("prototype_cars_list_general.html", rows=rows)

