from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:240702@localhost:5432/rental_cars"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models.populate_database import *
from views.orders_view import *
from views.clients_view import *
from views.cars_view import *


if __name__ == "__main__":
    app.run()
