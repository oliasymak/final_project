# final_project
Final project of the external course

You can find my app here:
https://rentalcarepam1.herokuapp.com/

How to build this project:

Navigate to the project root folder

Install the requirements:

pip install -r requirements.txt



Set the following environment variables:

APP_SETTINGS=config.ProductionConfig
SECRET_KEY=<your_secret_key>

Configure PostgreSQL database

DATABASE_URL=postgres://<your_username>:<your_password>@<your_database_url>/<your_database_name>

Run migrations to create database infrastructure:

python -m flask db upgrade

(Optional) Populate the database with sample data

python populate_db.py

Run the project locally:

python -m flask run
