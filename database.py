from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


db = SQLAlchemy()

def create_database(app):
    with app.app_context():
        db.init_app(app)
        print(f"Connecting to database")

        inspector = inspect(db.engine)

        table_names = ['characters', 'houses', 'strengthes']

        all_tables_exist = True
        for table_name in table_names:
            if not inspector.has_table(table_name):
                all_tables_exist = False
                break

        if all_tables_exist:
            print('Database already exists, skipping table creation.')
        else:
            try:
                # These imports are required for SQLAlchemy to create the tables
                from models import Character, House, Strength
                db.create_all()
                print('Database and tables created!')
            except Exception as e:
                print(f'Error creating tables: {e}.')
            