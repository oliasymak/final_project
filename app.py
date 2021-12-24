from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import os
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.populate_database import *
from views.orders_view import *
from views.clients_view import *
from views.cars_view import *

if __name__ == "__main__":
    app.run()
