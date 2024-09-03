import fastavro
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from api import Departments, Jobs, HiredEmployees
import datetime
 
# ct stores current time
ct = datetime.datetime.now()

def table_to_avro(table_name, model, file_name):
    # Initialize database session
    engine = create_engine('sqlite:///FLASK-API/instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query all data from the table
    data = session.query(model).all()

    # Define the AVRO schema
    schema = {
        'doc': f'{table_name} data',
        'name': table_name,
        'namespace': 'my.avro.namespace',
        'type': 'record',
        'fields': [
            {'name': column.name, 'type': 'int' if column.type.python_type == int else 'string'}
            for column in model.__table__.columns
        ]
    }

    # Convert SQLAlchemy objects to dictionaries
    records = [{column.name: getattr(row, column.name) for column in model.__table__.columns} for row in data]

    # Write to AVRO file
    with open(file_name, 'wb') as out:
        fastavro.writer(out, schema, records)

    session.close()

table_to_avro('jobs', Jobs, f'jobs_{ct}.avro')
table_to_avro('departments', Departments, f'departments_{ct}.avro')
table_to_avro('hired_employees', HiredEmployees, f'hired_employees_{ct}.avro')
