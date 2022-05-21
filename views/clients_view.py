from app import app
from app import db
from flask import render_template, request
from flask import redirect
from flask import url_for
from service.clients_service import *


@app.route('/clients_list', methods=["GET", "POST"])
def clients_list():
    '''
    The functions returns the page with table ClientsList
    Parameters:
    rows (class): table ClientsList
    :return: prototype_clients_list_general.html
    '''
    rows = clients_table()
    if request.method == "GET":
        return render_template("prototype_clients_list_general.html", rows=rows)
    return redirect(url_for('clients_list'))


@app.route('/add_client', methods=["GET", "POST"])
def add_client():
    '''
    The function returns the layout of the add client page
    :return: prototype_add_client.html
    '''
    if request.method == "GET":
        return render_template("prototype_add_client.html")
    return redirect(url_for('add_client'))


@app.route('/clients_list_add', methods=["GET", "POST"])
def clients_list_add():
    '''
    The function adds a new item to the client database,
    returns a page with an updated client table
    if entered data is not correct, function return page with error
    Parameters:
    first_name (string): data from the field first name
    last_name (string): data from the field last name
    passport_number  (int): data from the field passport number
    add_date (string): data from the field add date
    rows (class): table of clients
    :return: prototype_clients_list_general.html
    '''
    if request.method == "POST":
        first_name = request.form.get('cname').strip()
        last_name = request.form.get('cdes').strip()
        passport_number = request.form.get('rtime').strip()
        add_date = request.form.get('calendar')

    if first_name == '' or last_name == '' or passport_number == '' or add_date == '':
        return render_template("prototype_data_not_correct.html")
    if first_name.isdigit() or last_name.isdigit() or passport_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    if len(passport_number) > 6:
        return render_template("prototype_data_not_correct.html")
    client_add(first_name, last_name, passport_number, add_date)
    rows = clients_table()
    return render_template("prototype_clients_list_general.html", rows=rows)



@app.route('/edit_client', methods=["GET", "POST"])
def edit_client():
    '''
    The function returns the layout of the edit client page
    :return: prototype_edit_client.html
    '''
    if request.method == "GET":
        return render_template("prototype_edit_client.html")
    return redirect(url_for('edit_client'))


@app.route('/clients_list_edit', methods=["GET", "POST"])
def clients_list_edit():
    '''
    The function edit an item of the clients table with selected passport number,
    returns a page with an updated clients table,
    edit date in table Orders if it is needed
    if entered data is not correct, function return page with error
    Parameters:
    ffirst_name (string): data from the field first name
    llast_name (string): data from the field last name
    ppassport_number  (string): data from the field passport number
    aadd_date (string): data from the field add date
    select_client (string): data from the field selected client
    rows (class): table of clients
    :return: prototype_clients_list_general.html
    '''
    if request.method == "POST":
        ffirst_name = request.form.get('cname').strip()
        llast_name = request.form.get('cdes').strip()
        ppassport_number = request.form.get('rtime').strip()
        aadd_date = request.form.get('calendar')
        select_client = request.form.get('passport').strip()
    if ffirst_name == '' or llast_name == '' or ppassport_number == '' or aadd_date == '':
        return render_template("prototype_data_not_correct.html")
    if ffirst_name.isdigit() or llast_name.isdigit() or ppassport_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    if len(ppassport_number) > 6:
        return render_template("prototype_data_not_correct.html")
    if ClientsList.query.get(select_client) == None:
        return render_template("prototype_data_not_correct.html")
    client_edit(ffirst_name, llast_name, ppassport_number, aadd_date, select_client)
    # rows = db.session.query(ClientsList)
    rows = clients_table()
    return render_template("prototype_clients_list_general.html", rows=rows)

@app.route('/refresh_сlient', methods=["GET", "POST"])
def refresh_client():
    '''
    The function filters client in the range of entered dates,
    return the page with table of clients with this elements
    If date from is empty the function return the page with all elements by some date
    If date by is empty the function return the page with all elements from some date till the end
    If date by and from is empty the function return the page with all elements
    Parameters:
    date_from (string): data from field date from
    date_by (string): data from field by
    :return:prototype_clients_list_general.html
    '''
    if request.method == "POST":
        date_from = request.form.get('calendar1')
        date_by = request.form.get('calendar2')
    if date_from == '' and date_by == '':
        rows = clients_table()
        return render_template("prototype_clients_list_general.html", rows=rows)
    if date_from == '':
        from1 = db.session.query(ClientsList).order_by(ClientsList.add_date)
        rows = db.session.query(ClientsList).filter(ClientsList.add_date.between(from1[0].add_date, date_by))
        return render_template("prototype_clients_list_general.html", rows=rows)
    if date_by == '':
        from1 = db.session.query(ClientsList).order_by(ClientsList.add_date)
        rows = db.session.query(ClientsList).filter(ClientsList.add_date.between(date_from, from1[-1].add_date))
        return render_template("prototype_clients_list_general.html", rows=rows)
    rows = db.session.query(ClientsList).filter(ClientsList.add_date.between(date_from, date_by))
    return render_template("prototype_clients_list_general.html", rows=rows)


@app.route('/client_delete', methods=["GET", "POST"])
def client_delete():
    '''
        The function delete client from cars table using passport number,
        delete order with this client
        return page with updated clients table
        if entered data is not correct, function return page with error
        Parameters:
        ppassport_number (string): data from field passport number
        rows: clients table
        :return: prototype_clients_list_general.html
    '''
    if request.method == "POST":
        ppassport_number = request.form.get('cdes').rstrip()
    if ClientsList.query.get(ppassport_number) == None:
        return render_template("prototype_data_not_correct.html")
    if ppassport_number.isdigit():
        return render_template("prototype_data_not_correct.html")
    client_delete_f(ppassport_number)

    rows = clients_table()

    return render_template("prototype_clients_list_general.html", rows=rows)


@app.route('/client_statistic', methods=["GET", "POST"])
def client_statistic():
    if request.method == "GET":
        return render_template("client_statistic.html")
    return redirect(url_for('client_statistic'))


@app.route('/clients_statistic_passport', methods=["GET", "POST"])
def clients_statistic_passport():
    '''
    The function returns a page with diagram
    :return:
    '''
    stat_client_passport()
    if request.method == "GET":
        return render_template("stat_client_passport.html")


@app.route('/clients_statistic_date', methods=["GET", "POST"])
def clients_statistic_date():
    '''
    The function returns a page with diagram
    :return:
    '''
    stat_client_date()
    if request.method == "GET":
        return render_template("stat_client_date.html")

@app.route('/search_client_by_name', methods=["GET", "POST"])
def search_client_by_name():
    '''
    The function search elements
    :return:
    '''
    if request.method == "POST":
        clnt_name = request.form.get('clnt_name').strip()

    names = clnt_name.split(" ")
    print(names)
    if clnt_name.isdigit():
        return render_template("prototype_data_not_correct.html")
    rows = db.session.query(ClientsList).filter_by(first_name=names[0], last_name = names[1])
    return render_template("prototype_clients_list_general.html", rows=rows)

@app.route('/search_client_by_passport_number', methods=["GET", "POST"])
def search_client_by_passport_number():
    if request.method == "POST":
        clnt_pasnum = request.form.get('clnt_pasnum').strip()
    if clnt_pasnum.isdigit():
        return render_template("prototype_data_not_correct.html")
    if len(clnt_pasnum) > 6:
        return render_template("prototype_data_not_correct.html")
    rows = db.session.query(ClientsList).filter_by(passport_number=clnt_pasnum)
    return render_template("prototype_clients_list_general.html", rows=rows)




