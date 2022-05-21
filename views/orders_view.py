from app import app
from app import db
from flask import render_template, request
from flask import redirect
from flask import url_for
from service.orders_service import *

@app.route('/')
def index():
    '''
    the function returns the layout of the order table
    Parameters:
    rows (class): OrdersList database sorted in ascending order
    :return: prototype_orders_list_general.html
    '''
    rows = orders_table()
    return render_template("prototype_orders_list_general.html", rows=rows)

@app.route('/orders_list', methods=["GET", "POST"])
def orders_list():
    '''
    the function returns the layout of the order table
    Parameters:
    rows (class): OrdersList database sorted in ascending order
    :return: prototype_orders_list_general.html
    '''
    rows = orders_table()
    if request.method == "GET":
        return render_template("prototype_orders_list_general.html", rows=rows)
    return redirect(url_for('orders_list'))

@app.route('/add_order', methods=["GET", "POST"])
def add_order():
    '''
    The function returns the layout of the add order page
    :return: prototype_add_order.html
    '''
    if request.method == "GET":
        return render_template("prototype_add_order.html")
    return redirect(url_for('add_order'))

@app.route('/orders_list_add', methods=["GET", "POST"])
def orders_list_add():
    '''
    The function adds a new item to the order database,
    updates the number of orders in the table customers and machines,
    returns a page with an updated order table
    if entered data is not correct, function return page with error
    Parameters:
    cpassport_number (string): data from the field passport number
    ccar_number (string): data from the field car number
    rental_time (int): data from the field rental time
    add_date (string): data from the field add date
    :return:
    '''
    if request.method == "POST":
        cpassport_number = request.form.get('cname').strip()
        ccar_number = request.form.get('cdes').strip()
        rental_time = request.form.get('rtime').strip()
        add_date = request.form.get('calendar')
    if cpassport_number == '' or ccar_number == '' or rental_time == '' or add_date == '':
        return render_template("prototype_data_not_correct.html")
    if len(cpassport_number) > 6:
        return render_template("prototype_data_not_correct.html")
    if len(ccar_number) > 8:
        return render_template("prototype_data_not_correct.html")
    if not rental_time.isdigit():
        return render_template("prototype_data_not_correct.html")
    if cpassport_number.isdigit() or ccar_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    if ClientsList.query.get(cpassport_number) == None:
        return render_template("prototype_data_not_correct.html")
    if CarsList.query.get(ccar_number) == None:
        return render_template("prototype_data_not_correct.html")
    order_add(ccar_number, cpassport_number, rental_time, add_date)
    rows = orders_table()
    return render_template("prototype_orders_list_general.html", rows=rows)


@app.route('/edit_order', methods=["GET", "POST"])
def edit_order():
    '''
    The function returns the layout of the edit order page
    :return: prototype_edit_order.html
    '''
    if request.method == "GET":
        return render_template("prototype_edit_order.html")
    return redirect(url_for('edit_order'))


@app.route('/orders_list_edit', methods=["GET", "POST"])
def orders_list_edit():
    '''
    The function edit an item of the order table with selected id,
    returns a page with an updated order table
    if entered data is not correct, function return page with error
    Parameters:
    ppassport_number (string): data from the field passport number
    ccar_namber (string): data from the field car number
    rrental_time  (string): data from the field rental cost
    aadd_date (string): data from the field add date
    select_order (string): data from the field selected order
    rows (class): table of orders
    :return: prototype_orders_list_general.html
    '''
    if request.method == "POST":
        ppassport_number = request.form.get('cname').strip()
        ccar_number = request.form.get('cdes').strip()
        rrental_time = request.form.get('rtime').strip()
        aadd_date = request.form.get('calendar')
        select_order = request.form.get('select_order')
    if ppassport_number == '' or ccar_number == '' or rrental_time == '' or aadd_date == '':
        return render_template("prototype_data_not_correct.html")
    if len(ppassport_number) > 6:
        return render_template("prototype_data_not_correct.html")
    if len(ccar_number) > 8:
        return render_template("prototype_data_not_correct.html")
    if not rrental_time.isdigit():
        return render_template("prototype_data_not_correct.html")
    if ppassport_number.isdigit() or ccar_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    if ClientsList.query.get(ppassport_number) == None:
        return render_template("prototype_data_not_correct.html")
    if CarsList.query.get(ccar_number) == None:
        return render_template("prototype_data_not_correct.html")
    if OrdersList.query.get(select_order) == None:
        return render_template("prototype_data_not_correct.html")
    order_edit(ppassport_number, ccar_number, rrental_time, aadd_date, select_order)
    rows = orders_table()
    return render_template("prototype_orders_list_general.html", rows=rows)

@app.route('/refresh_order', methods=["GET", "POST"])
def refresh_order():
    '''
    The function filters orders in the range of entered dates,
    return the table of orders with this elements
    If date from is empty the function return the page with all elements by some date
    If date by is empty the function return the page with all elements from some date till the end
    If date by and from is empty the function return the page with all elements
    Parameters:
    date_from (string): data from field date from
    date_by (string): data from field by
    :return:prototype_orders_list_general.html
    '''
    if request.method == 'POST':
        date_from = request.form.get('calendar1')  # запрос к данным формы
        date_by = request.form.get('calendar2')
    if date_from == '' and date_by == '':
        rows = db.session.query(OrdersList).order_by(OrdersList.id)
        return render_template("prototype_orders_list_general.html", rows=rows)
    if date_from == '':
        from1 = db.session.query(OrdersList).order_by(OrdersList.add_date)
        rows = db.session.query(OrdersList).filter(OrdersList.add_date.between(from1[0].add_date, date_by)).order_by(
            OrdersList.id)
        return render_template("prototype_orders_list_general.html", rows=rows)
    if date_by == '':
        from1 = db.session.query(OrdersList).order_by(OrdersList.add_date)
        rows = db.session.query(OrdersList).filter(OrdersList.add_date.between(date_from, from1[-1].add_date)).order_by(
            OrdersList.id)
        return render_template("prototype_orders_list_general.html", rows=rows)
    rows = db.session.query(OrdersList).filter(OrdersList.add_date.between(date_from, date_by)).order_by(OrdersList.id)
    return render_template("prototype_orders_list_general.html", rows=rows)


@app.route('/order_delete', methods=["GET", "POST"])
def order_delete():
    '''
    The function delete selected order from orders table using id
    if entered data is not correct, function return page with error
    return page with updated orders table
    Parameters:
    order_id (string): data from field id
    rows: orders table
    :return: prototype_orders_list_general.html
    '''
    if request.method == "POST":
        order_id = request.form.get('cdes').strip()
    if OrdersList.query.get(order_id) == None:
        return render_template("prototype_data_not_correct.html")
    if not order_id.isdigit():
        return render_template("prototype_data_not_correct.html")
    order_delete_f(order_id)
    rows = orders_table()

    return render_template("prototype_orders_list_general.html", rows=rows)

@app.route('/order_statistic', methods=["GET", "POST"])
def order_statistic():
    '''
    The function returns the statistic of order table
    :return: prototype_add_order.html
    '''
    if request.method == "GET":
        return render_template("order_statistic.html")
    return redirect(url_for('order_statistic'))

@app.route('/orders_statistic_car', methods=["GET", "POST"])
def orders_statistic_car():
    '''
    The function returns a page with diagram
    :return:
    '''
    stat_order_car()
    if request.method == "GET":
        return render_template("stat_order_car.html")

@app.route('/orders_statistic_client', methods=["GET", "POST"])
def orders_statistic_client():
    '''
    The function returns a page with diagram
    :return:
    '''
    stat_order_client()
    if request.method == "GET":
        return render_template("stat_order_client.html")

@app.route('/orders_statistic_date', methods=["GET", "POST"])
def orders_statistic_date():
    '''
    The function returns a page with diagram
    :return:
    '''
    stat_order_date()
    if request.method == "GET":
        return render_template("stat_order_date.html")

@app.route('/search_order_by_id', methods=["GET", "POST"])
def search_order_by_id():
    '''
    The function search elements
    :return:
    '''
    if request.method == "POST":
        id_number = request.form.get('ord_id').strip()
    if not id_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    rows = db.session.query(OrdersList).filter_by(id=int(id_number))
    return render_template("prototype_orders_list_general.html", rows=rows)

@app.route('/search_order_by_car_number', methods=["GET", "POST"])
def search_order_by_car_number():
    '''
    The function search elements
    :return:
    '''
    if request.method == "POST":
        car_num = request.form.get('ord_cnum').strip()
    if car_num.isdigit():
        return render_template("prototype_data_not_correct.html")
    if len(car_num) != 8:
        return render_template("prototype_data_not_correct.html")
    rows = db.session.query(OrdersList).filter_by(car_number=car_num)
    return render_template("prototype_orders_list_general.html", rows=rows)

@app.route('/search_order_by_passport_number', methods=["GET", "POST"])
def search_order_by_passport_number():
    '''
    The function search elements
    :return:
    '''
    if request.method == "POST":
        ord_pasnum = request.form.get('ord_pasnum').strip()
    if ord_pasnum.isdigit():
        return render_template("prototype_data_not_correct.html")
    if len(ord_pasnum) > 6:
        return render_template("prototype_data_not_correct.html")
    rows = db.session.query(OrdersList).filter_by(client_passport_number=ord_pasnum)
    return render_template("prototype_orders_list_general.html", rows=rows)




